"""Offline relative Markdown links and GitHub-style heading anchors."""

import html
import re
from urllib.parse import unquote, urlsplit


def prose(text):
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def anchors(text):
    text = prose(text)
    found = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    for heading in re.findall(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        heading = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", heading)
        heading = html.unescape(re.sub(r"<[^>]*>", "", heading)).lower()
        base = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        slug, suffix = base, 0
        while slug in found:
            suffix += 1
            slug = f"{base}-{suffix}"
        found.add(slug)
    return found


def link_errors(document, root):
    text = prose(document.read_text(encoding="utf-8"))
    targets = re.findall(r"\]\(([^)]+)\)", text)
    targets += re.findall(r"^ {0,3}\[[^]]+\]:\s+(\S+)", text, re.M)
    errors = []
    for raw in targets:
        target = raw.strip().split(' "', 1)[0].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        name = unquote(parsed.path)
        path = (root / name.lstrip("/")) if name.startswith("/") else document.parent / name
        if not name:
            path = document
        if not path.exists():
            errors.append(f"{document}: missing target {target}")
        elif parsed.fragment and path.suffix.lower() == ".md":
            if unquote(parsed.fragment) not in anchors(path.read_text(encoding="utf-8")):
                errors.append(f"{document}: missing anchor {target}")
    return errors


def public_documents(root):
    documents = [root / "README.md", root / "AGENTS.md"]
    for folder in ["docs", "skills", "benchmarks"]:
        documents.extend(p for p in (root / folder).rglob("*.md") if ".contextlean" not in p.parts)
    return sorted(set(documents))
