# TODO
# add new link to posts

import os

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
    post_title["id"] = "post_title"
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


def make_post_page(md_filename: str):
    post_content = make_post(md_filename)
    title = get_by_id(post_content, "post_title")
    html_filename = md_filename.replace(".md", ".html")
    create_page(post_content, title, html_filename)


def create_post_list_page():
    files = os.listdir("./pages/")
    posts = [file for file in files if file.startswith("post")]
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



def create_main_nav():
    mainfiles = os.listdir(MAIN)
    base = readfile(BASEFILE)
    for file in mainfiles:
        mainfile = os.path.join(MAIN, file)
        main = readfile(mainfile)
        pagefile = os.path.join(PAGES, file)
        make_page(base, main, "Saeed", pagefile)

    mdfiles = os.listdir(MARKDOWN)
    for mdfile in mdfiles:
        md_content = readfile(os.path.join(MARKDOWN, mdfile))
        post_file = os.path.join(os.path.join(POSTS, mdfile.replace(".md", ".html")))
        # make_post(base, md_content, "post", post_file)


def main():
    # change_main_nav()
    # prepare_post("post_001.md")
    # prepare_page()
    create_post_list_page()


if __name__ == "__main__":
    main()
