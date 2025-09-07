# src/main.py
import os
import sys
import shutil

from copystatic import copy_files_recursive
from sitegen import generate_pages_recursive

DIR_STATIC = "./static"
DIR_BUILD  = "./docs"          # <- GitHub Pages default
DIR_CONTENT = "./content"
TEMPLATE = "./template.html"

def main():
    # Basepath aus CLI, Default "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print(f"Deleting build directory {DIR_BUILD} ...")
    if os.path.exists(DIR_BUILD):
        shutil.rmtree(DIR_BUILD)

    print("Copying static files to build directory...")
    copy_files_recursive(DIR_STATIC, DIR_BUILD)

    print("Generating pages recursively...")
    generate_pages_recursive(
        dir_path_content=DIR_CONTENT,
        template_path=TEMPLATE,
        dest_dir_path=DIR_BUILD,
        basepath=basepath,
    )

if __name__ == "__main__":
    main()
