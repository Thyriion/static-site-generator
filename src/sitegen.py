# sitegen.py
import os
from utility import markdown_to_html_node

def extract_title(markdown: str) -> str:
    """
    Findet die erste H1-Überschrift (eine einzelne #) und gibt ihren Text zurück.
    Wenn keine vorhanden ist, wird ValueError geworfen.
    """
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("##"):
            return stripped[2:].strip()
        if stripped.startswith("#") and not stripped.startswith("##"):
            # erlaubt "#Title" ohne Leerzeichen
            return stripped.lstrip("#").strip()
    raise ValueError("No H1 title found in markdown")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Markdown → HTML
    root = markdown_to_html_node(md_content)
    html_content = root.to_html()

    # Titel extrahieren
    title = extract_title(md_content)

    # Platzhalter ersetzen
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Zielordner anlegen falls nötig
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)

    print(f"✅ Wrote page: {dest_path}")

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    """
    Läuft rekursiv durch dir_path_content.
    Für jede .md-Datei wird eine gleichnamige .html unter dest_dir_path erzeugt,
    wobei die Verzeichnisstruktur beibehalten wird.
    content/index.md            -> public/index.html
    content/blog/post.md        -> public/blog/post.html
    """
    if not os.path.isdir(dir_path_content):
        raise FileNotFoundError(f"Content directory not found: {dir_path_content}")
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    for root, _dirs, files in os.walk(dir_path_content):
        rel = os.path.relpath(root, dir_path_content)  # "." oder z.B. "blog"
        out_dir = dest_dir_path if rel == "." else os.path.join(dest_dir_path, rel)
        os.makedirs(out_dir, exist_ok=True)

        for fname in files:
            if not fname.lower().endswith(".md"):
                continue
            src_md = os.path.join(root, fname)
            stem = os.path.splitext(fname)[0]
            out_html_name = "index.html" if stem == "index" else f"{stem}.html"
            dest_html = os.path.join(out_dir, out_html_name)
            generate_page(src_md, template_path, dest_html)
