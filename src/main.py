import os
import posixpath
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

# dir_path_static = "./static"
# dir_path_public = "./public"

# f_path = "./content"
# t_path = '.'
# d_path = './public'

from pathlib import Path
dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"
p = Path(dir_path_content)
markdown_paths = list(p.glob('**/*.md'))

    
def main():

    # print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    # print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    
    print("Generating page...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

    # for path in markdown_paths:
    #     dir_name = posixpath.dirname(path)
    #     # print(f'dir/base_name: {dir_name}:::{base_name}')
    #     # print(f'mds path[1]: {path}')
    #     split_dir_names = dir_name.split('/')
    #     # print(f'split: {split_dir_names}')
    #     # print(f'{"/".join(split_dir_names[1:])}')
    #     needed_dir = "/".join(split_dir_names[1:])
    #     # print(f'{needed_dir}')
    #     generate_page(
    #         # os.path.join(dir_path_content, "index.md"),##!orginal
    #         # os.path.join(mds_path[0]),
    #         path,
    #         template_path,##!orginal
    #         # os.path.join(dir_path_public, "index.html"),##!orginal ##!./public
    #         # os.path.join("./public/contact/", "index.html"), ##!what is suppose to be
    #         os.path.join(dir_path_public, needed_dir, "index.html"),
    #     )

if __name__ == '__main__':
    main()
