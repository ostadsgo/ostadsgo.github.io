# TODO
# script and css are different for each directory like pages, and posts
# if base changed I have to recreate all pages so I have to use markdown file
#     or I have to save main part of pages in separate directory and create
#     pages again

import os

import markdown


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


def md_to_html(md: str) -> str:
    return markdown.markdown(md)


def make_post(base: str, main: str, **kwargs) -> str:
    title = kwargs.get("title", "None")
    css = kwargs.get("css", "None")
    js = kwargs.get("js", "None")
    links = readfile("./includes/post_nav.html")
    main = f"<article class='post'>{main}</article>"
    return (
        base.replace("$css", css)
        .replace("$js", js)
        .replace("$title", title)
        .replace("$navlist", links)
        .replace("$content", main)
    )


def make_page(base: str, content: str, **kwargs) -> str:
    title = kwargs.get("title", "None")
    css = kwargs.get("css", "None")
    js = kwargs.get("js", "None")
    links = readfile("./includes/nav.html")
    return (
        base.replace("$css", css)
        .replace("$js", js)
        .replace("$title", title)
        .replace("$navlist", links)
        .replace("$content", content)
    )


def prepare_post():
    # Values for template
    basefile = "./pages/base.html"
    htmlfile = "./posts/first_serious_app.html"
    mdfile = "./markdown/first_serious_app.md"
    extra = dict(
        title="اولین برنامه جدی با پایتون",
        css="../static/css/style.css",
        js="../static/js/script.css",
    )

    # Files
    base = readfile(basefile)
    md = readfile(mdfile)
    main = md_to_html(md)

    # Gernerate new html with required data
    htmlcontent = make_post(base, main, **extra)
    print(htmlcontent)
    writefile(htmlfile, htmlcontent)


def prepare_page():
    basefile = "./main/base.html"
    htmlfile = "./pages/blog.html"
    extra = dict(
        title="اولین برنامه جدی با پایتون",
        css="../static/css/style.css",
        js="../static/js/script.css",
    )

    # Files
    base = readfile(basefile)
    main = readfile(htmlfile)

    # Gernerate new html with required data
    htmlcontent = make_page(base, main, **extra)
    print(htmlcontent)
    writefile(htmlfile, htmlcontent)


def add_new_link():
    mainfiles = os.listdir("./main")
    base = readfile("./base/base.html")
    for file in mainfiles:
        mainfile = f"./main/{file}"
        main = readfile(mainfile)
        extra = dict(
            title="اولین برنامه جدی با پایتون",
            css="../static/css/style.css",
            js="../static/js/script.css",
        )
        html = make_page(base, main, **extra)
        pagefile = f"./pages/{file}"
        writefile(pagefile, html)
        



def main():
    add_new_link()


if __name__ == "__main__":
    main()
