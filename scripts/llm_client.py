"""Azure OpenAI vision API calls for screenshot extraction."""

from __future__ import annotations

import base64
import io
import json
import time
from pathlib import Path

from openai import AzureOpenAI, BadRequestError, OpenAI, RateLimitError, APIError
from PIL import Image

from .config import CHAT_MODEL

SYSTEM_PROMPT_TEMPLATE = """You are an expert at analyzing screenshots from a UiPath automation workshop tutorial.
Your task is to extract structured metadata from each screenshot.

The screenshot is from the lesson: "{lesson_title}"
Exercise: "{exercise_name}"

Lesson context:
---
{lesson_context}
---

For the given screenshot, provide the following three types of analysis:

1. **ocr_text**: Extract ALL visible text from the screenshot exactly as it appears, preserving layout where possible. Include menu items, labels, buttons, field values, tooltips, and any other readable text. If text is partially obscured, indicate with [...].

2. **description**: A concise description (2-4 sentences) of what the screenshot shows. Identify the UiPath platform component visible (e.g., Agent Builder, Studio Web, Orchestrator, Action Center, BPMN designer, IXP). Describe the state of the UI — what panels are open, what is configured, what data is visible.

3. **step_instructions**: Based on the visual state and any highlighted or active elements in the screenshot, describe the step(s) the user should take. Focus on:
   - What UI element is selected, highlighted, or has focus
   - What button to click, what field to fill in, what menu to open
   - Use the format: "Click on...", "In the ... field, enter...", "Select ... from..."
   - If multiple steps are visible, list them in order

   If the screenshot is purely informational (showing results, a diagram, or a completed state), write "Informational screenshot — no user action required." and describe what it shows instead.

Respond with a JSON object containing exactly these three keys: "ocr_text", "description", "step_instructions". Do not include any text outside the JSON."""


def encode_image(image_path: Path) -> tuple[str, str]:
    """Read and base64-encode an image file.

    For animated GIFs, extracts the first frame and converts to PNG.

    Returns:
        Tuple of (base64_data, media_type).
    """
    suffix = image_path.suffix.lower()

    if suffix == ".gif":
        img = Image.open(image_path)
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return b64, "image/png"

    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }
    media_type = media_types.get(suffix, "image/png")

    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    return b64, media_type


def build_prompt(
    lesson_title: str,
    exercise_name: str,
    lesson_context: str,
) -> str:
    """Build the system prompt with context injected."""
    return SYSTEM_PROMPT_TEMPLATE.format(
        lesson_title=lesson_title,
        exercise_name=exercise_name,
        lesson_context=lesson_context,
    )


# Newer models (e.g. gpt-5.x) reject a non-default `temperature` outright. We
# cannot know from the deployment name alone, so the first call probes it and the
# result is cached here for the rest of the run.
_SUPPORTS_TEMPERATURE = True


def extract_from_image(
    client: OpenAI | AzureOpenAI,
    image_path: Path,
    system_prompt: str,
    max_retries: int = 3,
) -> tuple[dict, dict]:
    """Call the Azure OpenAI vision API to extract metadata from an image.

    Args:
        client: Azure OpenAI client.
        image_path: Path to the image file.
        system_prompt: System prompt with context.
        max_retries: Maximum retry attempts on rate limit errors.

    Returns:
        Tuple of (extraction_dict, usage_dict).

    Raises:
        RuntimeError: If the API call fails after all retries.
    """
    b64_data, media_type = encode_image(image_path)

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Analyze this screenshot and extract metadata as specified.",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{media_type};base64,{b64_data}",
                        "detail": "high",
                    },
                },
            ],
        },
    ]

    last_error = None
    for attempt in range(max_retries):
        try:
            global _SUPPORTS_TEMPERATURE
            kwargs = {
                "model": CHAT_MODEL,
                "messages": messages,
                "max_completion_tokens": 4000,
                "response_format": {"type": "json_object"},
            }
            if _SUPPORTS_TEMPERATURE:
                kwargs["temperature"] = 0.2

            try:
                response = client.chat.completions.create(**kwargs)
            except BadRequestError as e:
                # Decide from THIS request's kwargs, not the shared flag: with
                # concurrency>1 several calls are in flight when the first one
                # clears the flag, and gating on it would leave them unretried.
                if "temperature" in kwargs and "temperature" in str(e):
                    if _SUPPORTS_TEMPERATURE:
                        print("  Model rejects temperature=0.2; retrying at the default.")
                    _SUPPORTS_TEMPERATURE = False
                    kwargs.pop("temperature", None)
                    response = client.chat.completions.create(**kwargs)
                else:
                    raise

            content = response.choices[0].message.content
            extraction = json.loads(content)

            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

            return extraction, usage

        except RateLimitError as e:
            last_error = e
            wait = 2 ** (attempt + 1)
            print(f"  Rate limited, waiting {wait}s before retry...")
            time.sleep(wait)

        except json.JSONDecodeError as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"  Invalid JSON response, retrying...")
                time.sleep(1)
            else:
                raise RuntimeError(
                    f"Failed to parse JSON response after {max_retries} attempts: {e}"
                ) from e

        except APIError as e:
            last_error = e
            if e.status_code and e.status_code >= 500:
                wait = 2 ** (attempt + 1)
                print(f"  Server error ({e.status_code}), waiting {wait}s...")
                time.sleep(wait)
            else:
                raise

    raise RuntimeError(
        f"Failed after {max_retries} retries: {last_error}"
    )
