#!/usr/bin/env python3
"""
Generate the just-the-docs sidebar from the directory tree.

Writes `_includes/nav_tree.html`, which `_includes/components/site_nav.html`
renders in place of the theme's front-matter-driven navigation. No markdown
file needs front matter: titles come from each file's first H1, folders come
from directories, and a folder's README.md (if any) is the folder's own page.

Usage:
    python scripts/gen_nav.py
"""

from __future__ import annotations

import html
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "_includes" / "nav_tree.html"
# Placeholder swapped for `site.baseurl` by `_includes/components/site_nav.html`.
BASE = "@@BASE@@"

# Keep in sync with the `update_index` target in the Makefile.
EXCLUDED_ROOT = re.compile(r"^(index|README|wip)\.md$")
EXCLUDED_ANY = re.compile(r"(^|/)\.|(^|/)(AGENTS|CLAUDE|SKILL)\.md$|node_modules/")

LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")


@dataclass
class Folder:
    files: dict[str, str] = field(default_factory=dict)  # file name -> repo path
    dirs: dict[str, "Folder"] = field(default_factory=dict)
    readme: str | None = None


def list_markdown() -> list[str]:
    out = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            "*.md",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return sorted(
        p
        for p in set(out)
        if (ROOT / p).is_file()
        and not EXCLUDED_ROOT.match(p)
        and not EXCLUDED_ANY.search(p)
    )


def title_of(path: str) -> str | None:
    """First H1 outside fenced code blocks, with links and backticks flattened."""
    in_fence = False
    text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
        elif not in_fence and re.match(r"# +\S", line):
            title = LINK_RE.sub(r"\1", line[1:].strip()).replace("`", "")
            return re.sub(r"\s*#+\s*$", "", title) or None
    return None


def prettify(dirname: str) -> str:
    name = re.sub(r"^\d+-", "", dirname).replace("-", " ").replace("_", " ")
    return name[:1].upper() + name[1:]


def build_tree(paths: list[str]) -> Folder:
    root = Folder()
    for path in paths:
        *dirs, name = path.split("/")
        node = root
        for d in dirs:
            node = node.dirs.setdefault(d, Folder())
        if name in ("README.md", "index.md"):
            node.readme = path
        else:
            node.files[name] = path
    return root


def url_of(path: str) -> str:
    # GitHub Pages (jekyll-readme-index) serves README.md as the folder URL.
    if path.endswith(("/README.md", "/index.md")):
        url = "/" + path[: path.rindex("/") + 1]
    else:
        url = "/" + path[: -len(".md")] + ".html"
    return BASE + quote(url)


def link(path: str, title: str) -> str:
    # Exact shape matters: the theme's no-JS "current page" CSS matches
    # `<a href="…" class="nav-list-link">`.
    return f'<a href="{url_of(path)}" class="nav-list-link">{html.escape(title)}</a>'


def has_content(node: Folder) -> bool:
    return bool(node.files or node.readme or any(has_content(d) for d in node.dirs.values()))


def render(node: Folder, indent: int) -> list[str]:
    pad = "  " * indent
    lines: list[str] = []

    for name in sorted(node.files):
        path = node.files[name]
        title = title_of(path) or name[: -len(".md")]
        lines.append(f'{pad}<li class="nav-list-item">{link(path, title)}</li>')

    for dirname in sorted(node.dirs):
        child = node.dirs[dirname]
        if not has_content(child):
            continue
        label = (title_of(child.readme) if child.readme else None) or prettify(dirname)
        has_children = bool(child.files or any(has_content(d) for d in child.dirs.values()))

        lines.append(f'{pad}<li class="nav-list-item">')
        if has_children:
            lines.append(
                f'{pad}  <button class="nav-list-expander btn-reset" aria-label="{html.escape(label)} submenu" aria-expanded="false">'
                '<svg viewBox="0 0 24 24" aria-hidden="true"><use xlink:href="#svg-arrow-right"></use></svg></button>'
            )
        if child.readme:
            lines.append(f"{pad}  {link(child.readme, label)}")
        else:
            # No page of its own: the label just toggles the folder.
            lines.append(
                f'{pad}  <a href="#" class="nav-list-link nav-folder" '
                f'onclick="this.previousElementSibling.click();return false;">{html.escape(label)}</a>'
            )
        if has_children:
            lines.append(f'{pad}  <ul class="nav-list">')
            lines.extend(render(child, indent + 2))
            lines.append(f"{pad}  </ul>")
        lines.append(f"{pad}</li>")

    return lines


def main() -> None:
    tree = build_tree(list_markdown())
    body = [
        "{% comment %} Generated by scripts/gen_nav.py. Do not edit by hand. {% endcomment %}",
        "{% raw %}",
        '<ul class="nav-list">',
        f'  <li class="nav-list-item"><a href="{BASE}/" class="nav-list-link">Home</a></li>',
        *render(tree, 1),
        "</ul>",
        "{% endraw %}",
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(body) + "\n", encoding="utf-8")
    print(f"[+] wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
