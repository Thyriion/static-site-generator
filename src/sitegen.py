# sitegen.py
import os
from utility import markdown_to_html_node
from typing import Optional

def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        s = line.strip()
        if s.startswith("# ") and not s.startswith("##"):
            return s[2:].strip()
        if s.startswith("#") and not s.startswith("##"):
            return s.lstrip("#").strip()
    raise ValueError("No H1 title found in markdown")

def _normalize_basepath(basepath: str) -> str:
    # immer mit führendem UND abschließendem Slash
    if not basepath:
        return "/"
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath = basepath + "/"
    # Spezialfall Root: "///" etc. normalisieren
    return "/" if basepath == "//" else basepath

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str = "/") -> None:
    basepath = _normalize_basepath(basepath)
    print(f"Generating page from {from_path} to {dest_path} using {template_path} (basepath={basepath})")

    with open(from_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    root = markdown_to_html_node(md_content)
    html_content = root.to_html()
    title = extract_title(md_content)

    page = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
    )

    # WICHTIG: Basepath für absolute Links (href="/..., src="/...) injizieren
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/',  f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"✅ Wrote page: {dest_path}")

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = "/") -> None:
    basepath = _normalize_basepath(basepath)
    if not os.path.isdir(dir_path_content):
        raise FileNotFoundError(f"Content directory not found: {dir_path_content}")
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    for root, _dirs, files in os.walk(dir_path_content):
        rel = os.path.relpath(root, dir_path_content)  # "." oder z. B. "blog"
        out_dir = dest_dir_path if rel == "." else os.path.join(dest_dir_path, rel)
        os.makedirs(out_dir, exist_ok=True)

        for fname in files:
            if not fname.lower().endswith(".md"):
                continue
            src_md = os.path.join(root, fname)
            stem = os.path.splitext(fname)[0]
            out_html_name = "index.html" if stem == "index" else f"{stem}.html"
            dest_html = os.path.join(out_dir, out_html_name)
            generate_page(src_md, template_path, dest_html, basepath=basepath)
