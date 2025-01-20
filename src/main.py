
import os
import shutil
from markdown import markdown_to_html_node

#yes, copytree fuction exists
#just so i can play with fileio
def copy_folder_to(src, dest):

    if(os.path.exists(dest)):
        shutil.rmtree(dest)

    os.mkdir(dest)
    
    def copy_recursion(src, dest):
        files = os.listdir(src)

        for file in files:
            path = "/" + file
            if os.path.isfile(src + path):
                shutil.copy(src+path, dest+path)
            else:
                os.mkdir(dest+path)
                copy_recursion(src+path, dest+path)

    copy_recursion(src, dest)

def extract_title(markdown:str):
    if not markdown.startswith("#"):
        raise Exception("Missing header")

    ss = markdown.split("\n")
    ss[0] = ss[0].strip("# ")
    return ss[0]
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    def read_from (file_path):
        file = open(file_path)
        r = file.read()
        file.close()
        return r

    md_from_path = read_from(from_path)
    html_template_path = read_from(template_path)

    result = markdown_to_html_node(md_from_path)
    result_in_html = result.to_html()

    title = extract_title(md_from_path)
    html_template_path = html_template_path.replace("{{ Title }}", title)
    html_template_path = html_template_path.replace("{{ Content }}", result_in_html)

    new_file = open(dest_path, "x")
    new_file.write(html_template_path)
    new_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):  
    files = os.listdir(dir_path_content)

    for file in files:
        path = "/" + file
        if os.path.isfile(dir_path_content + path):
            if not path.endswith(".md"):
                continue
            output_file = path.replace(".md", ".html")
            generate_page(dir_path_content + path, template_path, dest_dir_path + output_file)
        else:
            os.mkdir(dest_dir_path+path)
            generate_pages_recursive(dir_path_content + path, template_path, dest_dir_path + path)
    pass

def main():
    cwd = os.getcwd()
    copy_folder_to(cwd+"/static", cwd+"/public")

    #generate_page(cwd+"/content/index.md", cwd+"/template.html", cwd+"/public/index.html")
    generate_pages_recursive(cwd+"/content/", cwd+"/template.html", cwd+"/public/")

main()