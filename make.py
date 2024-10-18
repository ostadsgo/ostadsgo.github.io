# TODO
# add new link to posts

import os

import markdown

BASE_DIR = os.path.dirname(__file__)
PAGES = os.path.join(BASE_DIR, "pages")
MAIN = os.path.join(BASE_DIR, "main")
INCLUDES = os.path.join(BASE_DIR, "includes")
POSTS = os.path.join(BASE_DIR, "posts")
MARKDOWN = os.path.join(BASE_DIR, "markdown")

STATIC = os.path.join(BASE_DIR, "static")

BASE = os.path.join(BASE_DIR, "base")
BASEFILE = os.path.join(BASE, "base.html")

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
            print(f"{filename} created")
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


def make_post(base: Html, content: Markdown, title: str, filename: str):
    content = md_to_html(content)
    content = f"<article class='post'>{content}</article>"
    links = readfile("./includes/nav.html")
    kwargs = {
        "title": title,
        "links": links,
        "content": content,
    }
    html = make_template(base, **kwargs)
    writefile(filename, html)
    print(f"Create {filename}")


def make_page(base: Html, content: Html, title: str, filename: str):
    links = readfile("./includes/nav.html")
    kwargs = {
        "title": title,
        "links": links,
        "content": content,
    }
    html = make_template(base, **kwargs)
    writefile(filename, html)
    print(filename)


def prepare_post():
    filename = "post_001"
    title = "post"
    post = readfile(os.path.join(MARKDOWN, f"{filename}.md"))
    base = readfile(BASEFILE)
    htmlfile = os.path.join(POSTS, f"{filename}.html")
    make_post(base, post, title, htmlfile)


def prepare_page():
    filename = "projects.html"
    title = "Project | پروژه"
    content_file = os.path.join(MAIN, filename)
    content = readfile(content_file)
    base = readfile(BASEFILE)
    htmlfile = os.path.join(PAGES, f"{filename}")
    make_page(base, content, title, htmlfile)


def change_main_nav():
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
        make_post(base, md_content, "post", post_file) 


def main():
    change_main_nav()
    # prepare_page()


if __name__ == "__main__":
    main()

