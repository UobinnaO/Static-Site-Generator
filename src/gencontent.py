import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path
import posixpath
import shutil
# dir_path_static = "./static"
# dir_path_public = "./public"
# dir_path_content = "./content"
# template_path = "./template.html"

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            dir_name = posixpath.dirname(from_path)
            # print(f'dir/base_name: {dir_name}:::{base_name}')
            # print(f'mds path[1]: {path}')
            split_dir_names = dir_name.split('/')
            # print(f'split: {split_dir_names}')
            # print(f'{"/".join(split_dir_names[2:])}')
            needed_dir = "/".join(split_dir_names[2:])
            # print(f'from path = dir_path_content + filename({filename}): {from_path}')
            # print(f'dest path = dest_dir_path + filename({filename}): {dest_path}')
            # print(f'needed dir: {needed_dir}')
            # print(dest_dir_path, needed_dir, "index.html")
            generate_page(
            # os.path.join(mds_path[0]),
            from_path,
            template_path,##!orginal
            # os.path.join(dir_path_public, "index.html"),##!orginal ##!./public
            # os.path.join("./public/contact/", "index.html"), ##!what is suppose to be
            os.path.join(dest_dir_path, needed_dir, "index.html"),
           )
        else:
            generate_pages_recursive(from_path, template_path, dest_dir_path)

    # p = Path(dir_path_content)
    # markdown_paths = list(p.glob('**/*.md'))

    # dir_name = posixpath.dirname(markdown_paths[0])
    # # print(f'dir/base_name: {dir_name}:::{base_name}')
    # # print(f'mds path[1]: {path}')
    # split_dir_names = dir_name.split('/')
    # # print(f'split: {split_dir_names}')
    # # print(f'{"/".join(split_dir_names[1:])}')
    # needed_dir = "/".join(split_dir_names[1:])
    # # print(f'{needed_dir}')
    # generate_page(
    #     # os.path.join(dir_path_content, "index.md"),##!orginal
    #     # os.path.join(mds_path[0]),
    #     markdown_paths[0],
    #     template_path,##!orginal
    #     # os.path.join(dir_path_public, "index.html"),##!orginal ##!./public
    #     # os.path.join("./public/contact/", "index.html"), ##!what is suppose to be
    #     os.path.join(dest_dir_path, needed_dir, "index.html"),
    # )



def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    print(f'\nmd chars: {markdown_content[:30]}')
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    # print(f'\nhtml chars: {template[:30]}')
    # print(f'\nhtml: {template}')

    print(f'dest path(provided): {dest_path}')
    dest_dir_path = os.path.dirname(dest_path)
    print(f'dest dir path: {dest_dir_path}')
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)
    print(f'#######\nNEW RUN\n######')

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")


