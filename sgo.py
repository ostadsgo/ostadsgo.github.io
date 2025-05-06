#! /uelsr/bin/python


import os
import shutil
import sys
from pathlib import Path

import markdown
from bs4 import BeautifulSoup
from pygments.formatters import HtmlFormatter


class File:
    # File paths
    BASE_DIR = Path(__file__).parent
    STATIC = Path("./static")

    @classmethod
    def read(cls, filename: str) -> str:
        content = ""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError as e:
            print(f"{filename} not found. {e}")
        except Exception as e:
            print(f"Unkown error happend! {e}")
        return content

    @classmethod
    def write(cls, filename: str, content: str) -> bool:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
                print(f"{filename} created successfuly.")
                return True
        except FileNotFoundError as e:
            print(f"{filename} not found. {e}")
        except Exception as e:
            print(f"Unkown error happend! {e}")
        finally:
            return False

# Create styles for code highlight
formatter = HtmlFormatter(style='github-dark')
with open('static/css/pygments.css', 'w') as f:
    f.write(formatter.get_style_defs('.codehilite')) 

class Component:
    PATH = File.BASE_DIR / "templates"

    def __init__(self, filename: str):
        self.template = File.read(str(self.PATH / filename))
        self.html = self.template

    def render(self, data: dict[str, str]):
        self.html = self.template.format(**data)
        return self.html


class Page:
    def __init__(self, title, content):
        self.title = title
        self.nav = Component("nav.html")
        self.footer = Component("footer.html")
        self.content = content

    def create(self, filename):
        base = File.read("templates/base.html")
        kw = {
            "title": self.title,
            "nav": self.nav.html,
            "content": self.content,
            "footer": self.footer.html,
        }
        self.content = base.format(**kw)
        File.write(f"./pages/{filename}", self.content)


class Post:
    def __init__(self, post_name):
        md = File.read(f"./posts/{post_name}")
        html = markdown.markdown(md, extensions=['fenced_code', 'codehilite'])
        self.soup = BeautifulSoup(html, "html.parser")
        self.link = f"/pages/{post_name.replace('.md', '.html')}"
        self.date, self.mins, self.tag = self.get_info()
        self.title = self.get_title()
        self.summary = self.get_summary()

    def get_title(self):
        tag = self.soup.find("h1")
        if tag:
            return tag.text.strip()
        return "Title of the post not found!"

    def get_info(self):
        tag = self.soup.find_all("p")
        if tag:
            return tag[0].text.split("•")
        return "Summary of the post not  found!"

    def get_summary(self):
        tag = self.soup.find_all("p")
        if tag:
            return tag[1].text.strip()
        return "Summary of the post not  found!"


class PostHeader(Component):
    def __init__(self, post_name):
        filename = "post_header.html"
        super().__init__(filename)
        post = Post(post_name)
        data = {
            "post_link": post.link,
            "post_title": post.title,
            "date": post.date,
            "mins": post.mins,
            "tag": post.tag,
        }
        self.render(data)

    @classmethod
    def all(cls):
        articles = []
        files = sorted(os.listdir("./posts"), reverse=True)
        for file in files:
            article = PostHeader(file)
            articles.append(article.html)
        return "\n".join(articles)


class PostSummary(Component):
    def __init__(self, post_name):
        filename = "post_summary.html"
        super().__init__(filename)
        post = Post(post_name)
        data = {
            "post_link": post.link,
            "post_title": post.title,
            "date": post.date,
            "mins": post.mins,
            "tag": post.tag,
            "post_summary": post.summary,
        }
        self.render(data)

    @classmethod
    def get(cls, number=3):
        articles = []
        files = sorted(os.listdir("./posts"), reverse=True)
        for file in files[:number]:
            article = PostSummary(file)
            articles.append(article.html)
        return "\n".join(articles)


class PostPage(Page):
    def __init__(self, md):
        filename = md.replace(".md", ".html")
        post = Post(md)
        md = File.read(f"./posts/{md}")
        html = markdown.markdown(md)
        template = Component("post.html")
        data = {"post": html}
        content = template.render(data)
        super().__init__(post.title, content)
        self.create(filename)

    @classmethod
    def create_all(cls):
        files = os.listdir("./posts")
        for file in files:
            PostPage(file)

    @classmethod
    def create_last(cls):
        posts = os.listdir("./posts")
        pages = os.listdir("./pages")

        for md_file in posts:
            filename = md_file.split(".")[0]
            if filename not in pages:
                PostPage(md_file)
                print(f"{md_file} created as page.")

    @classmethod
    def create_by_name(cls, name):
        PostPage(name)
        print(f"{name} created as page.")


class AboutPage(Page):
    def __init__(self):
        self.title = "درباره من"
        self.filename = "about.html"
        self.content = Component(self.filename).html
        super().__init__(self.title, self.content)
        self.create(self.filename)


class BlogPage(Page):
    def __init__(self):
        self.title = "بلاگ"
        self.filename = "blog.html"
        template = Component(self.filename)
        data = {"articles": PostHeader.all()}
        content = template.render(data)
        super().__init__(self.title, content)
        self.create(self.filename)


class IndexPage(Page):
    def __init__(self):
        title = "سعید غلامی | Saeed Gholami"
        filename = "index.html"
        template = Component("index.html")
        data = {"articles": PostSummary.get(3)}
        content = template.render(data)
        super().__init__(title, content)

        if os.path.exists(filename):
            os.remove(filename)

        self.create(filename)
        shutil.move(f"./pages/{filename}", "./")


class Command:
    @classmethod
    def build(cls):
        IndexPage()
        AboutPage()
        BlogPage()
        PostPage.create_all()
        print("Build all pages.")

    @classmethod
    def update(cls):
        """build  only dynamic parts . and post that not created."""
        IndexPage()
        BlogPage()
        PostPage.create_last()

    @classmethod
    def publish(cls):
        os.system("git add -A")
        os.system('git commit -m "Update and publish"')
        os.system("git push")
        print("Published successfuly.")


def main():
    if len(sys.argv) < 2:
        print("Usage: sgo [<update>, <publish>]")
        return
    if sys.argv[1] == "build":
        Command.build()
    elif sys.argv[1] == "update":
        Command.update()
    elif sys.argv[1] == "publish":
        Command.publish()
    else:
        print("Unknown operation.")


if __name__ == "__main__":
    main()
