"""MkDocs hook: compile slide decks the same way MkDocs compiles modules.

    docs/slides/<slug>.md                      ->  site/slides/<slug>.html
    docs/slides/tier1/<name>.part.html         ->  site/slides/<name>.html

Nothing generated is ever written into docs/. Run `mkdocs build` or
`mkdocs serve` and the decks come with the site.

Authoring syntax:  course-design/deck-authoring.md
Visual identity:   decks/deck.css  (the :root token block, and only there)
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import markdown
from mkdocs.structure.files import File

HERE = Path(__file__).resolve().parent

MD_EXTENSIONS = ["tables", "def_list", "attr_list", "sane_lists", "footnotes"]

FONTS = (
    "https://fonts.googleapis.com/css2"
    "?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800"
    "&family=Caveat:wght@600;700"
    "&family=IBM+Plex+Mono:wght@400;600"
    "&family=Instrument+Sans:wght@400;500;600"
    "&display=swap"
)

# --------------------------------------------------------------------------
# icons: senior-design vocabulary, usable as :client: inline or on a callout
# --------------------------------------------------------------------------

ICONS = {
    "client":     '<circle cx="12" cy="8" r="4" fill="none" stroke-width="2"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7" fill="none" stroke-width="2"/>',
    "team":       '<circle cx="8" cy="9" r="3" fill="none" stroke-width="2"/><circle cx="17" cy="10" r="2.5" fill="none" stroke-width="2"/><path d="M2 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5M15 20c0-2.6 1.6-4.4 4-4.4 1.6 0 3 .8 3 2.4" fill="none" stroke-width="2"/>',
    "agent":      '<rect x="4" y="7" width="16" height="12" rx="4" fill="none" stroke-width="2"/><path d="M12 3v4" stroke-width="2"/><circle cx="9" cy="13" r="1.4"/><circle cx="15" cy="13" r="1.4"/>',
    "repo":       '<path d="M5 4h11l3 3v13H5z" fill="none" stroke-width="2"/><path d="M8 9h8M8 13h8M8 17h5" stroke-width="2"/>',
    "checkpoint": '<path d="M4 4v16" stroke-width="2"/><path d="M4 5h13l-2.5 4L17 13H4z" fill="none" stroke-width="2"/>',
    "studio":     '<path d="M3 19h18" stroke-width="2"/><rect x="5" y="6" width="14" height="9" rx="2" fill="none" stroke-width="2"/>',
    "risk":       '<path d="M12 3l9.5 17H2.5z" fill="none" stroke-width="2"/><path d="M12 9v5" stroke-width="2"/><circle cx="12" cy="17" r="1.2"/>',
    "spec":       '<path d="M6 3h8l4 4v14H6z" fill="none" stroke-width="2"/><path d="M14 3v4h4" fill="none" stroke-width="2"/><path d="M9 12h6M9 16h6" stroke-width="2"/>',
    "ship":       '<path d="M3 15l9-9 9 9" fill="none" stroke-width="2"/><path d="M6 15v5h12v-5" fill="none" stroke-width="2"/>',
    "bug":        '<ellipse cx="12" cy="13" rx="5" ry="6" fill="none" stroke-width="2"/><path d="M7 10L4 8M17 10l3-2M7 16l-3 2M17 16l3 2M12 7V4" stroke-width="2"/>',
    "clock":      '<circle cx="12" cy="12" r="9" fill="none" stroke-width="2"/><path d="M12 7v5l3 2" fill="none" stroke-width="2"/>',
    "question":   '<circle cx="12" cy="12" r="9" fill="none" stroke-width="2"/><path d="M9 9.5a3 3 0 115 2.3c-.9.7-2 1.2-2 2.7" fill="none" stroke-width="2"/><circle cx="12" cy="17.5" r="1.1"/>',
    "key":        '<circle cx="8" cy="12" r="4" fill="none" stroke-width="2"/><path d="M12 12h9M18 12v3M15 12v2" stroke-width="2"/>',
    "warn":       '<path d="M12 3l9.5 17H2.5z" fill="none" stroke-width="2"/><path d="M12 9v5" stroke-width="2"/><circle cx="12" cy="17" r="1.2"/>',
    "joke":       '<circle cx="12" cy="12" r="9" fill="none" stroke-width="2"/><path d="M8 14c1 1.6 2.4 2.4 4 2.4s3-.8 4-2.4" fill="none" stroke-width="2"/><circle cx="9" cy="10" r="1.2"/><circle cx="15" cy="10" r="1.2"/>',
}

CALLOUT_ICON = {"key": "key", "ask": "question", "warn": "warn", "ai": "agent", "joke": "joke"}
CALLOUT_TAG = {"key": "Key point", "ask": "Ask the room", "warn": "Pitfall", "ai": "The agent", "joke": ""}


def icon_svg(name: str) -> str:
    body = ICONS.get(name)
    if not body:
        return ""
    return (
        '<svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" '
        f'fill="none">{body}</svg>'
    )


# --------------------------------------------------------------------------
# front matter
# --------------------------------------------------------------------------

def split_front_matter(text: str) -> tuple[dict, str]:
    meta: dict[str, str] = {}
    if not text.startswith("---"):
        return meta, text
    end = text.find("\n---", 3)
    if end == -1:
        return meta, text
    for line in text[3:end].strip("\n").splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta, text[end + 4:].lstrip("\n")


# --------------------------------------------------------------------------
# protect fenced blocks so the slide splitter never cuts through code
# --------------------------------------------------------------------------

FENCE_RE = re.compile(r"^```([A-Za-z0-9_+-]*)[ \t]*$")


def protect_fences(text: str) -> tuple[str, list[str]]:
    out: list[str] = []
    blocks: list[str] = []
    lines = text.split("\n")
    n = 0
    while n < len(lines):
        m = FENCE_RE.match(lines[n])
        if not m:
            out.append(lines[n])
            n += 1
            continue
        lang = m.group(1).lower()
        body: list[str] = []
        n += 1
        while n < len(lines) and not FENCE_RE.match(lines[n]):
            body.append(lines[n])
            n += 1
        n += 1  # closing fence
        raw = "\n".join(body)
        if lang == "mermaid":
            blocks.append(f'<pre class="mermaid">{html.escape(raw)}</pre>')
        else:
            cls = f' class="language-{lang}"' if lang else ""
            blocks.append(f"<pre><code{cls}>{html.escape(raw)}</code></pre>")
        out.append(f"@@FENCE{len(blocks) - 1}@@")
    return "\n".join(out), blocks


def restore_fences(html_text: str, blocks: list[str]) -> str:
    def sub(m: re.Match) -> str:
        return blocks[int(m.group(1))]
    html_text = re.sub(r"<p>\s*@@FENCE(\d+)@@\s*</p>", sub, html_text)
    return re.sub(r"@@FENCE(\d+)@@", sub, html_text)


# --------------------------------------------------------------------------
# ::: blocks
# --------------------------------------------------------------------------

BLOCK_OPEN = re.compile(r"^:::\s*([a-z]+)\s*(.*)$")


def parse_blocks(lines: list[str]) -> list[tuple[str, str, list[str]]]:
    """Flat list of (kind, arg, lines). kind '' means plain markdown."""
    out: list[tuple[str, str, list[str]]] = []
    buf: list[str] = []
    n = 0
    while n < len(lines):
        m = BLOCK_OPEN.match(lines[n].strip())
        if not m:
            buf.append(lines[n])
            n += 1
            continue
        if buf:
            out.append(("", "", buf))
            buf = []
        kind, arg = m.group(1), m.group(2).strip()
        body: list[str] = []
        n += 1
        while n < len(lines) and lines[n].strip() != ":::":
            body.append(lines[n])
            n += 1
        n += 1
        out.append((kind, arg, body))
    if buf:
        out.append(("", "", buf))
    return out


def md(text: str) -> str:
    return markdown.markdown(text, extensions=MD_EXTENSIONS, output_format="html5")


def inline_icons(text: str) -> str:
    def sub(m: re.Match) -> str:
        name = m.group(1)
        if name not in ICONS:
            return m.group(0)
        return f'<span class="ico-inline">{icon_svg(name)}</span>'
    return re.sub(r":([a-z]{3,12}):", sub, text)


def wrap_tables(text: str) -> str:
    return re.sub(r"(<table>.*?</table>)", r'<div class="tablewrap">\1</div>', text, flags=re.S)


def add_steps(html_text: str) -> str:
    """Give each top-level <li> (or each direct child block) a data-step."""
    if html_text.strip().startswith(("<ul>", "<ol>")):
        depth = 0
        count = 0
        out: list[str] = []
        for token in re.split(r"(<ul>|</ul>|<ol>|</ol>|<li>)", html_text):
            if token in ("<ul>", "<ol>"):
                depth += 1
                out.append(token)
            elif token in ("</ul>", "</ol>"):
                depth -= 1
                out.append(token)
            elif token == "<li>":
                if depth == 1:
                    count += 1
                    out.append(f'<li data-step="{count}">')
                else:
                    out.append(token)
            else:
                out.append(token)
        return "".join(out)

    parts = re.findall(r"<(p|div|figure|pre|blockquote|h3)\b.*?</\1>", html_text, flags=re.S)
    n = 0
    for part in parts:
        n += 1
        tag = re.match(r"<(\w+)", part).group(1)
        html_text = html_text.replace(part, part.replace(f"<{tag}", f'<{tag} data-step="{n}"', 1), 1)
    return html_text


def render_body(lines: list[str]) -> tuple[str, str]:
    note_html = ""
    chunks: list[str] = []

    for kind, arg, body in parse_blocks(lines):
        text = "\n".join(body).strip("\n")

        if kind == "":
            if text.strip():
                chunks.append(wrap_tables(md(text)))
        elif kind == "note":
            note_html += md(text)
        elif kind in CALLOUT_ICON:
            tag = arg or CALLOUT_TAG.get(kind, "")
            tag_html = f'<span class="tag">{html.escape(tag)}</span>' if tag else ""
            chunks.append(
                f'<div class="callout {kind}"><span class="ico">{icon_svg(CALLOUT_ICON[kind])}</span>'
                f'<div class="body">{tag_html}{wrap_tables(md(text))}</div></div>'
            )
        elif kind == "steps":
            chunks.append(add_steps(wrap_tables(md(text))))
        elif kind == "cols":
            cells = [c.strip() for c in text.split("|||")]
            cls = "cols c3" if len(cells) >= 3 else "cols"
            inner = "".join(f"<div>{wrap_tables(md(c))}</div>" for c in cells)
            chunks.append(f'<div class="{cls}">{inner}</div>')
        elif kind == "panel":
            chunks.append(f'<div class="panel">{wrap_tables(md(text))}</div>')
        else:
            chunks.append(wrap_tables(md(text)))

    return "".join(chunks), note_html


# --------------------------------------------------------------------------
# slide splitting
# --------------------------------------------------------------------------

HEADING_ATTR = re.compile(r"^(.*?)\s*\{([^}]*)\}\s*$")


def split_slides(body: str) -> list[dict]:
    slides: list[dict] = []
    cur: dict | None = None

    for raw in body.split("\n"):
        is_break = raw.strip() == "---"
        is_h1 = raw.startswith("# ")
        is_h2 = raw.startswith("## ")

        if is_h1 or is_h2 or is_break:
            if cur is not None:
                slides.append(cur)
            cur = {"title": "", "level": 1 if is_h1 else 2, "classes": [], "lines": []}
            if is_break:
                cur["level"] = 0
                continue
            title = raw[2:] if is_h1 else raw[3:]
            m = HEADING_ATTR.match(title)
            if m:
                title = m.group(1)
                cur["classes"] = [t[1:] for t in m.group(2).split() if t.startswith(".")]
            cur["title"] = title.strip()
            continue

        if cur is None:
            cur = {"title": "", "level": 0, "classes": [], "lines": []}
        cur["lines"].append(raw)

    if cur is not None:
        slides.append(cur)
    return [s for s in slides if s["title"] or "".join(s["lines"]).strip()]


# --------------------------------------------------------------------------
# assembly
# --------------------------------------------------------------------------

BANNER = """<!--
  ============================================================
   GENERATED BY decks/hook.py DURING `mkdocs build`.
   Source:   docs/slides/{src}
   Restyle:  decks/deck.css  (the :root token block)
   Syntax:   course-design/deck-authoring.md
  ============================================================
-->"""

SHELL = """<!doctype html>
{banner}
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<style>
{css}
</style>
</head>
<body>
<div id="stage">
{slides}
</div>
<div id="bar"><span></span></div>
<div id="notes"><div class="who" id="noteswho"></div><div class="txt" id="notestxt"></div></div>
<div id="blackout"></div>
<div id="grid"></div>
<div id="help"><div class="card">
  <button class="close" aria-label="Close">&times;</button>
  <h2>{title}</h2>
  <dl>
    <dt><kbd>&rarr;</kbd> <kbd>space</kbd> <kbd>PgDn</kbd></dt><dd>Next step or slide</dd>
    <dt><kbd>&larr;</kbd> <kbd>PgUp</kbd></dt><dd>Back</dd>
    <dt><kbd>&darr;</kbd> <kbd>S</kbd></dt><dd>Skip to the next slide</dd>
    <dt><kbd>O</kbd></dt><dd>Overview of all slides</dd>
    <dt><kbd>N</kbd></dt><dd>Speaker notes</dd>
    <dt><kbd>B</kbd></dt><dd>Black the screen</dd>
    <dt><kbd>Ctrl</kbd>+<kbd>P</kbd></dt><dd>Print / PDF handout, one slide per page</dd>
  </dl>
</div></div>
<script src="vendor/mermaid.min.js"></script>
<script>
{js}
</script>
</body>
</html>
"""

TIER1_SHELL = """<!doctype html>
{banner}
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head}
</head>
<body>
{body}
</body>
</html>
"""

HEAD_TAGS = re.compile(r"(<title>.*?</title>|<link\b[^>]*>|<style>.*?</style>)", re.S | re.I)


def banner_for(src: str) -> str:
    return "\n".join(line.rstrip() for line in BANNER.format(src=src).split("\n"))


def render_deck(src: Path) -> str:
    meta, body = split_front_matter(src.read_text(encoding="utf-8"))
    body, fences = protect_fences(body)

    deck_title = meta.get("title") or src.stem.replace("-", " ").title()
    module = meta.get("module", "").strip()
    week = meta.get("week", "").strip()
    day = meta.get("day", "").strip()

    raw_slides = split_slides(body)
    parts: list[str] = []

    for n, s in enumerate(raw_slides):
        content, note = render_body(s["lines"])
        content = inline_icons(restore_fences(content, fences))
        note = restore_fences(note, fences)

        classes = ["slide"] + s["classes"]
        head = ""
        if s["level"] == 1:
            classes += ["title-slide", "center"]
            head = f'<h1>{html.escape(s["title"])}</h1>'
        elif s["level"] == 2 and s["title"]:
            head = f'<h2>{html.escape(s["title"])}</h2><div class="rule"></div>'

        chip = f'<span class="chip">WEEK {html.escape(week)}</span>' if week else ""
        chip_day = f"<span>{html.escape(day)}</span>" if day else ""
        modlink = ""
        if module:
            modlink = (
                f'<a class="modlink" href="../modules/{module}/">'
                f"Full detail: the {html.escape(module.replace('-', ' '))} module &rarr;</a>"
            )

        parts.append(
            f'<section class="{" ".join(classes)}" data-note="{html.escape(note, quote=True)}">'
            f'<div class="chrome-top">{chip}{chip_day}</div>'
            f'<div class="content">{head}{content}</div>'
            f'<div class="chrome-bot">{modlink}<span>{n + 1} / {len(raw_slides)}</span></div>'
            f"</section>"
        )

    return SHELL.format(
        banner=banner_for(src.name),
        title=html.escape(deck_title),
        fonts=FONTS,
        css=(HERE / "deck.css").read_text(encoding="utf-8"),
        js=(HERE / "deck.js").read_text(encoding="utf-8"),
        slides="\n".join(parts),
    )


def render_tier1(src: Path) -> str:
    """Wrap a hand-authored fragment into a standalone document.

    The source is a fragment (no doctype/html/head/body) so the same file can be
    published as an Artifact, which supplies its own shell.
    """
    raw = src.read_text(encoding="utf-8")
    return TIER1_SHELL.format(
        banner=banner_for(f"tier1/{src.name}"),
        head="\n".join(HEAD_TAGS.findall(raw)),
        body=HEAD_TAGS.sub("", raw).strip(),
    )


# --------------------------------------------------------------------------
# the hook
# --------------------------------------------------------------------------

def on_files(files, config):
    src_dir = Path(config.docs_dir) / "slides"
    if not src_dir.is_dir():
        return files

    built = 0
    for deck in sorted(src_dir.glob("*.md")):
        files.append(
            File.generated(config, f"slides/{deck.stem}.html", content=render_deck(deck))
        )
        built += 1

    for part in sorted((src_dir / "tier1").glob("*.part.html")):
        name = part.name.replace(".part.html", ".html")
        files.append(
            File.generated(config, f"slides/{name}", content=render_tier1(part))
        )
        built += 1

    if built:
        import logging
        logging.getLogger("mkdocs").info("Built %d slide deck(s) into site/slides/", built)
    return files
