# TODO
# add new link to posts

import os
import shutil

import markdown
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(__file__)
PAGES = os.path.join(BASE_DIR, "pages")
MAIN = os.path.join(BASE_DIR, "main")
INCLUDES = os.path.join(BASE_DIR, "includes")
POSTS = os.path.join(BASE_DIR, "posts")
MARKDOWN = os.path.join(BASE_DIR, "markdown")

STATIC = os.path.join(BASE_DIR, "static")

TEMPLATES = os.path.join(BASE_DIR, "templates")
BASEFILE = os.path.join(TEMPLATES, "base.html")

Markdown = str
Html = str


def readfile(filename: str) -> str:
    content = ""
    try:
        with open(filename, "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        print(f"{filename} not found. {e}")
    except Exception as e:
        print(f"Unkown error happend! {e}")
    return content


def writefile(filename: str, content: str) -> bool:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            return True
    except FileNotFoundError as e:
        print(f"{filename} not found. {e}")
    except Exception as e:
        print(f"Unkown error happend! {e}")
    return False


def md_to_html(md: Markdown) -> str:
    return markdown.markdown(md)


def make_template(base: Html, **kwargs):
    return base.format(**kwargs)


def make_post(md_filename: str):
    md = readfile(f"./posts/{md_filename}")
    html = md_to_html(md)
    soup = BeautifulSoup(html, "html.parser")
    post_title = soup.find("h1")
    post_summary = soup.find("p")
    if isinstance(post_title, dict):
        post_title["id"] = "post_title"
    if isinstance(post_summary, dict):
        post_summary["id"] = "post_summary"
    template = readfile("./templates/post.html")
    kw = {"post": soup.prettify()}
    post_html = make_template(template, **kw)
    return post_html


def create_page(content: Html, title: str, filename: str):
    base = readfile("./templates/base.html")
    nav = readfile("./includes/nav.html")
    footer = readfile("./includes/footer.html")
    kw = {
        "title": title,
        "nav": nav,
        "content": content,
        "footer": footer,
    }
    html = make_template(base, **kw)
    file_path = f"./pages/{filename}"
    writefile(file_path, html)
    print(file_path, "is created")


def get_by_id(post: Html, element_id: str):
    result = ""
    soup = BeautifulSoup(post, "html.parser")
    element = soup.find(id=element_id)
    if element is not None:
        result = element.text.strip()
    return result


def create_post_page(md_filename: str):
    post_content = make_post(md_filename)
    title = get_by_id(post_content, "post_title")
    html_filename = md_filename.replace(".md", ".html")
    create_page(post_content, title, html_filename)


def get_posts():
    files = os.listdir("./pages/")
    posts = [file for file in files if file.startswith("post")]
    return posts

def create_post_list_page():
    posts = get_posts()
    for post in posts:
        post_page = readfile(f"./pages/{post}")
        soup = BeautifulSoup(post_page, "html.parser")
        title = soup.find(id="post_title")
        summary = soup.find(id="post_summary")
        new_soup = BeautifulSoup("<article class='post'></article>", "html.parser")
        new_soup.article.append(title)
        new_soup.article.append(summary)
        print(new_soup)
        create_page(new_soup.prettify(), "blog", "blog2.html")



def create_main_navs():
    mainfiles = os.listdir("./main")
    for file in mainfiles:
        mainfile = f"./main/{file}"
        content = readfile(mainfile)
        create_page(content, file.replace(".html", ""), file)

    mdfiles = os.listdir("./posts")
    for mdfile in mdfiles:
        create_post_page(mdfile)

def create_index():
    index_html = readfile("./main/index.html")
    create_page(index_html, "سعید غلامی", "index.html")
    shutil.move("./pages/index.html", "./index.html")


def main():
    # change_main_nav()
    # prepare_post("post_001.md")
    # prepare_page()
    # create_post_list_page()
    # create_main_navs()
    create_index()



if __name__ == "__main__":
    main()
