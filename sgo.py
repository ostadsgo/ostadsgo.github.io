#! /usr/bin/python
import os
import shutil
import sys
from pathlib import Path

import bs4
import markdown
from bs4 import BeautifulSoup


class File:
    # File paths
    BASE_DIR = Path(__file__).parent
    STATIC = Path("./static")

    @classmethod
    def read(cls, filename: str) -> str:
        content = ""
        try:
            with open(filename, "r") as f:
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
                return True
        except FileNotFoundError as e:
            print(f"{filename} not found. {e}")
        except Exception as e:
            print(f"Unkown error happend! {e}")
        finally:
            return False


class Template:
    PATH = File.BASE_DIR / "templates"

    @classmethod
    def build(cls, template, **kw):
        return template.format(**kw)


class Page:
    PATH = File.BASE_DIR / "pages"

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.build()

    def build(self):
        base = File.read("./templates/base.html")
        nav = File.read("./includes/nav.html")
        footer = File.read("./includes/footer.html")
        kw = {
            "title": self.title,
            "nav": nav,
            "content": self.content,
            "footer": footer,
        }
        self.content = Template.build(base, **kw)

    def create(self, filename):
        File.write(filename, self.content)


class Post:
    def __init__(self, filename):
        self.filename = filename
        md = File.read(self.filename)
        self.html = self.md_to_html(md)
        self.soup = BeautifulSoup(self.html, "html.parser")

    @classmethod
    def post_files(cls, number=-1):
        files = os.listdir("./posts/")
        post_files = sorted([file for file in files], reverse=True)
        if number > 0:
            return post_files[:number]
        return post_files

    def build(self):
        html_filename = self.filename.replace(".md", ".html")
        page = Page(self.filename, self.html)
        page.build()
        page.create(html_filename)

    @classmethod
    def create_all(cls):
        post_files = os.listdir("./posts")
        for post_file in post_files:
            post = File.read(f"./posts/{post_file}")
            html = markdown.markdown(post)
            page = Page("title", html)
            html_filename = post_file.replace(".md", ".html")
            page.create(f"./pages/{html_filename}")

    def md_to_html(self, filename):
        return markdown.markdown(filename)

    def get_tag_by_name(self, name):
        tag = self.soup.find(name)
        if isinstance(tag, bs4.element.Tag):
            return tag

    def title(self):
        tag = self.get_tag_by_name("h1")
        if tag:
            return tag.text
        return "post title not found"

    def summary(self):
        tag = self.get_tag_by_name("p")
        if tag:
            return tag.text
        return "post summary not found"


class Index:
    TITLE = "Saeed Gholami | سعید غلامی"
    FILENAME = "index.html"
    PATH = os.path.join("main", FILENAME)
    CONTENT = File.read(PATH)

    @classmethod
    def build(cls):
        content = cls.recent_posts()
        page = Page(cls.TITLE, content)
        page.create(cls.FILENAME)
        # shutil.move("./pages/index.html", "./index.html")
        print("index page created.")

    @classmethod
    def recent_posts(cls):
        """add 3 most recent posts in the index page."""
        posts = []
        post_files = Post.post_files(3)
        for post_file in post_files:
            post = Post(f"./posts/{post_file}")
            title = post.title()
            summary = post.summary()
            post_part = File.read("./templates/post_part.html")
            kw = {
                "post_title": title,
                "post_summary": summary,
                "date": "2020/2/12",
                "mins": "3 mins",
                "tag": "python",
            }
            post = Template.build(post_part, **kw)
            posts.append(post)
        recent_posts = "\n".join(posts)
        kw = {"recent_posts": recent_posts}
        index = Template.build(cls.CONTENT, **kw)
        return index






class Command:
    @classmethod
    def update(cls):
        """update neccessary parts."""
        # post = Post("./posts/post_001.md")
        # post.build()
        # Post.create_all()
        # Index.recent_posts()
        Index.build()

    @classmethod
    def build(cls):
        """build everything from scratch."""
        pass

    @classmethod
    def publish(cls):
        """publish to github page."""
        pass


def main():
    if len(sys.argv) < 2:
        print("Usage: sgo [<update>, <publish>]")
        return

    if sys.argv[1] == "update":
        Command.update()
    elif sys.argv[1] == "publish":
        Command.publish()
    else:
        print("Unknown operation.")


if __name__ == "__main__":
    main()
