"""Configuration and OpenAI client setup.

Supports two providers, chosen by which credentials are present in `scripts/.env`:

* **OpenAI** — set `OPENAI_API_KEY`. Models are addressed by their real model name
  (`OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL`).
* **Azure OpenAI** — set `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`. Models are
  addressed by *deployment* name, which is whatever you called the deployment in your
  resource and need not match the underlying model.

`OPENAI_API_KEY` wins if both are configured. Everything downstream passes `CHAT_MODEL` /
`EMBEDDING_MODEL` as the `model=` argument, which is correct for either provider.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI

# Project paths
SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent
DOCS_ROOT = PROJECT_ROOT / "docs"
CONTEXT_DIR = SCRIPTS_DIR / "context"
VECTOR_STORE_PATH = CONTEXT_DIR / "vector_store.json"

# Image processing constants
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif"}
METADATA_SUFFIX = ".metadata.json"
SKIP_DIRS = {"assets/images"}

# Load environment
load_dotenv(SCRIPTS_DIR / ".env")

# --- OpenAI ---------------------------------------------------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")
OPENAI_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# --- Azure OpenAI ---------------------------------------------------------
AZURE_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
AZURE_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "")
AZURE_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
AZURE_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-5.4")
AZURE_EMBEDDING_DEPLOYMENT = os.environ.get(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small"
)

# --- Resolved provider ----------------------------------------------------
PROVIDER = "openai" if OPENAI_API_KEY else "azure"

if PROVIDER == "openai":
    CHAT_MODEL = OPENAI_MODEL
    EMBEDDING_MODEL = OPENAI_EMBEDDING_MODEL
else:
    CHAT_MODEL = AZURE_DEPLOYMENT
    EMBEDDING_MODEL = AZURE_EMBEDDING_DEPLOYMENT


def validate_config() -> None:
    """Exit with a readable message if the chosen provider is not fully configured."""
    if OPENAI_API_KEY:
        return

    missing = []
    if not AZURE_ENDPOINT:
        missing.append("AZURE_OPENAI_ENDPOINT")
    if not AZURE_API_KEY:
        missing.append("AZURE_OPENAI_API_KEY")

    if missing:
        print(
            "Error: no OpenAI credentials found.\n"
            "  Either set OPENAI_API_KEY (plain OpenAI),\n"
            f"  or set the Azure variables — missing: {', '.join(missing)}."
        )
        print("Create scripts/.env from scripts/.env.example and fill in your credentials.")
        sys.exit(1)


def get_openai_client() -> OpenAI | AzureOpenAI:
    """Create and return a client for whichever provider is configured."""
    validate_config()
    if PROVIDER == "openai":
        return OpenAI(api_key=OPENAI_API_KEY)
    return AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
    )
