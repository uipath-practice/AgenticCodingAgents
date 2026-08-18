"""Harvest the Agentic Automation Google Site into source/ prose + staging images.

Image URLs on sites.google.com are short-lived (they 403 within minutes), so each
page's images are downloaded immediately after that page's HTML is fetched.
"""
import html as htmllib
import re, subprocess, sys, json
from pathlib import Path
import bs4

SITE = "https://sites.google.com/uipath.com/agentic-automation"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/140 Safari/537.36"

# Page order recovered from each page's "Next page" link.
PAGES = [
    ("home",                                        "home"),
    ("benefit-claims-processing",                   "index"),
    ("benefit-claims-processing/create-bpmn-process",                        "1-create-bpmn-process"),
    ("benefit-claims-processing/setting-up-the-solution",                    "2-setting-up-the-solution"),
    ("benefit-claims-processing/configure-a-robot",                          "3-configure-a-robot"),
    ("benefit-claims-processing/residency-verification-agent",               "4-residency-verification-agent"),
    ("benefit-claims-processing/income-verification-agent",                  "5-income-verification-agent"),
    ("benefit-claims-processing/eligibility-determination-agent",            "6-eligibility-determination-agent"),
    ("benefit-claims-processing/configure-human-validation",                 "7-configure-human-validation"),
    ("benefit-claims-processing/configure-api-integration-benefit-approval", "8-configure-api-integration-benefit-approval"),
    ("benefit-claims-processing/configure-api-integration-benefit-rejection","9-configure-api-integration-benefit-rejection"),
    ("next-steps",                                  "next-steps"),
]

SKIP_ANCESTORS = {"nav", "header", "footer"}
DROP_TEXT = re.compile(r"^(Next page|Previous page|Report abuse|Page details|Page updated|Got it|Learn more|"
                       r"Skip to main content|Skip to navigation|Search this site|Embedded Files|"
                       r"This site uses cookies from Google)")


def fetch(url):
    r = subprocess.run(["curl", "-sS", "-L", "-A", UA, url],
                       capture_output=True, text=True, check=True)
    return r.stdout


def in_chrome(el):
    p = el.parent
    while p is not None:
        if p.name in SKIP_ANCESTORS:
            return True
        cls = " ".join(p.get("class") or [])
        if "hUphyc" in cls or "lhbLEe" in cls or "JAPqpe" in cls:
            return True
        p = p.parent
    return False


def is_bold(el):
    """True if this element or an ancestor span sets font-weight >= 600."""
    p = el
    while p is not None and getattr(p, "get", None):
        m = re.search(r"font-weight:\s*(\d+|bold)", p.get("style") or "")
        if m:
            v = m.group(1)
            return v == "bold" or int(v) >= 600
        if p.name in ("p", "li", "h1", "h2", "h3", "h4"):
            break
        p = p.parent
    return False


def inline(el):
    """Render inline content of a block to markdown, preserving bold and links."""
    out = []
    for node in el.descendants:
        if not isinstance(node, bs4.element.NavigableString):
            continue
        txt = str(node)
        if not txt.strip():
            if out and not out[-1].endswith(" "):
                out.append(" ")
            continue
        txt = re.sub(r"\s+", " ", txt)
        # a link ancestor?
        a = node.find_parent("a")
        if a is not None and a.get("href"):
            href = a["href"]
            if "google.com/url?" in href:
                import urllib.parse
                q = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                href = q.get("q", [href])[0]
            out.append(f"[{txt.strip()}]({href})")
            continue
        if is_bold(node.parent):
            lead = " " if txt.startswith(" ") else ""
            trail = " " if txt.endswith(" ") else ""
            out.append(f"{lead}**{txt.strip()}**{trail}")
        else:
            out.append(txt)
    s = "".join(out)
    s = re.sub(r"\*\*\s*\*\*", " ", s)          # empty bold runs
    s = re.sub(r"\*\*([^*]+)\*\*\s*\*\*([^*]+)\*\*", r"**\1 \2**", s)  # merge adjacent bold
    return re.sub(r"\s+", " ", s).strip()


def embed_code(el) -> str:
    """Extract the payload of a Google Sites embed gadget.

    Sites stores "copy to clipboard" blocks -- prompts, JSON payloads -- in a
    `data-code` attribute rendered client-side into an iframe, so they are absent
    from the walked DOM text. The attribute is double HTML-escaped.
    """
    raw = htmllib.unescape(htmllib.unescape(el.get("data-code") or ""))
    txt = bs4.BeautifulSoup(raw, "html.parser").get_text("\n", strip=True)
    # The gadget appends its own copy-button label as the last line, and the
    # wording varies per block ("Copy to clipboard", "Copy this evaluation set").
    lines = txt.splitlines()
    while lines and re.match(r"^\s*Copy\b.*$", lines[-1]):
        lines.pop()
    return "\n".join(lines).strip()


class Harvester:
    def __init__(self, page_url):
        self.page_url = page_url
        self.images = []   # (index, url)
        self.lines = []

    def emit(self, text=""):
        if text or (self.lines and self.lines[-1] != ""):
            self.lines.append(text)

    def walk(self, el, depth=0, ordered=None, idx=None):
        for child in el.children:
            if isinstance(child, bs4.element.NavigableString):
                continue
            name = child.name
            cls = " ".join(child.get("class") or [])

            if child.has_attr("data-code"):
                code = embed_code(child)
                if code:
                    lang = "json" if code.lstrip().startswith(("{", "[")) else "text"
                    self.emit(); self.emit(f"```{lang}")
                    for line in code.splitlines():
                        self.lines.append(line)
                    self.emit("```"); self.emit()
                continue

            if name == "img" and "CENy8b" in cls:
                n = len(self.images) + 1
                self.images.append((n, child["src"]))
                self.emit(); self.emit(f"<<IMG:{n}>>"); self.emit()
                continue

            if name in ("script", "style", "svg", "nav", "header", "footer"):
                continue

            if name in ("h1", "h2", "h3", "h4") and "zfr3Q" in cls:
                if in_chrome(child):
                    continue
                txt = inline(child)
                if txt and not DROP_TEXT.match(txt):
                    lvl = {"h1": "#", "h2": "##", "h3": "###", "h4": "####"}[name]
                    self.emit(); self.emit(f"{lvl} {txt.replace('**','')}"); self.emit()
                continue

            if name in ("ol", "ul"):
                self.walk(child, depth + 1, ordered=(name == "ol"), idx=[0])
                self.emit()
                continue

            if name == "li":
                # a bare wrapper li holding only a nested list -> just recurse
                inner_list = child.find(["ol", "ul"], recursive=False)
                own = inline(child) if inner_list is None else inline_own_text(child)
                pad = "    " * max(0, depth - 1)
                if own and not DROP_TEXT.match(own):
                    if ordered:
                        idx[0] += 1
                        self.emit(f"{pad}{idx[0]}. {own}")
                    else:
                        self.emit(f"{pad}- {own}")
                for sub in child.find_all(["ol", "ul"], recursive=False):
                    self.walk(sub, depth + 1, ordered=(sub.name == "ol"), idx=[0])
                continue

            if name == "p" and "zfr3Q" in cls:
                if in_chrome(child):
                    continue
                txt = inline(child)
                if txt and not DROP_TEXT.match(txt):
                    self.emit(); self.emit(txt); self.emit()
                continue

            self.walk(child, depth, ordered, idx)


def inline_own_text(li):
    """Text of an li excluding nested lists."""
    clone = bs4.BeautifulSoup(str(li), "html.parser")
    for lst in clone.find_all(["ol", "ul"]):
        lst.decompose()
    return inline(clone)



def main():
    root = Path(__file__).resolve().parent.parent
    report = []
    for path, slug in PAGES:
        url = f"{SITE}/{path}"
        html = fetch(url)
        soup = bs4.BeautifulSoup(html, "html.parser")
        for t in soup(["script", "style"]):
            t.decompose()

        h = Harvester(url)
        h.walk(soup.body)

        # image destination
        if slug in ("home", "index", "next-steps"):
            imgdir = root / "staging" / "images" / (slug if slug != "index" else "_exercise-index")
        else:
            imgdir = root / "staging" / "images" / slug
        imgdir.mkdir(parents=True, exist_ok=True)

        ok = bad = 0
        for n, src in h.images:
            stem = re.sub(r"=[sw]\d+$", "", src)
            dest = imgdir / f"{n:02d}.png"
            r = subprocess.run(["curl", "-sS", "-L", "-A", UA, "-e", url, "-o", str(dest),
                                "-w", "%{http_code} %{content_type}", stem],
                               capture_output=True, text=True)
            code, _, ctype = r.stdout.partition(" ")
            if code == "200" and "image" in ctype:
                # fix extension to match real type
                ext = ".jpg" if "jpeg" in ctype else ".png" if "png" in ctype else ".gif" if "gif" in ctype else ".bin"
                final = imgdir / f"{n:02d}{ext}"
                if final != dest:
                    dest.rename(final)
                ok += 1
            else:
                bad += 1
                print(f"    !! image {n} HTTP {code} {ctype}", file=sys.stderr)

        # write prose
        if slug in ("home", "next-steps"):
            out = root / "staging" / "prose" / f"{slug}.md"
        elif slug == "index":
            out = root / "source" / "benefit-claims-processing" / "index.md"
        else:
            out = root / "source" / "benefit-claims-processing" / f"{slug}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        body = "\n".join(h.lines).strip() + "\n"
        body = re.sub(r"\n{3,}", "\n\n", body)
        header = (f"<!-- Harvested from {url}\n"
                  f"     Images: staging/images/{imgdir.name}/ ({len(h.images)} found)\n"
                  f"     <<IMG:n>> marks where image n appeared in the original page. -->\n\n")
        out.write_text(header + body, encoding="utf-8")
        report.append(dict(page=path, slug=slug, images=len(h.images), ok=ok, bad=bad,
                           words=len(body.split()), out=str(out.relative_to(root))))
        print(f"{slug:46} imgs {ok:3}/{len(h.images):3}  words {len(body.split()):5}  -> {out.relative_to(root)}")

    (root / "staging" / "harvest-report.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
