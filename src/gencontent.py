import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path
import posixpath

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            dir_name = posixpath.dirname(from_path)
            split_dir_names = dir_name.split('/')
            needed_dir = "/".join(split_dir_names[2:])
            generate_page(
            from_path,
            template_path,
            os.path.join(dest_dir_path, needed_dir, "index.html"),
            base_path   
           )
        else:
            generate_pages_recursive(from_path, template_path, dest_dir_path, base_path)


def generate_page(from_path, template_path, dest_path, base_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    # print(f'BEFORE REPLACE\n{template}')
    template = template.replace('href="/',f'href="{base_path}')
    template = template.replace('src="/',f'src="{base_path}')
    # print(f'AFTER REPLACE\n{template}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")


