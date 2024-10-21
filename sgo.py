#! /usr/bin/python

# TODO: Fix links of recent posts in index.page

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


class Component:
    PATH = File.BASE_DIR / "components"

    def __init__(self, html_file):
        self.html_file = html_file
        self.html = File.read(str(self.PATH / html_file))


class Nav(Component):
    def __init__(self, html_file):
        super().__init__(html_file)


class Footer(Component):
    def __init__(self, html_file):
        super().__init__(html_file)


class Intro(Component):
    def __init__(self, html_file):
        super().__init__(html_file)


class Article(Component):
    def __init__(self, html_file):
        super().__init__(html_file)
        self.title = ""
        self.summary = ""
        self.articles = []
        self.make()

    def make(self):
        post_files = os.listdir("./posts")
        for post_file in post_files:
            md = File.read(f"./posts/{post_file}")
            html = markdown.markdown(md)
            soup = BeautifulSoup(html, "html.parser")
            post_title_tag = soup.find("h1")
            p_tags = soup.find_all("p", limit=2)
            post_info = p_tags[0]
            post_summary_tag = p_tags[1]
            self.title = post_title_tag.text
            self.summary = post_summary_tag.text
            post_date, post_mins, post_tag = post_info.text.split("  ")
            post_file_html = post_file.replace(".md", ".html")
            kw = {
                "post_title": self.title,
                "post-link": f"./pages/{post_file_html}",
                "post_summary": self.summary,
                "date": post_date,
                "mins": post_mins,
                "tag": post_tag,
            }
            template = File.read("./templates/post_article.html")
            article = template.format(**kw)
            self.articles.append(article)

    def all(self):
        return self.articles

    def get(self, number=1):
        return self.articles[:number]

    def join(self, articles):
        return "\n".join(articles)


class Page:
    def __init__(self, title, content):
        self.title = title
        self.nav = Nav("nav.html")
        self.footer = Footer("footer.html")
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


class Post(Page):
    def __init__(self, md):
        self.filename = md.replace(".md", ".html")
        self.md = File.read(f"./posts/{md}")
        content = markdown.markdown(self.md)
        self.soup = BeautifulSoup(content, "html.parser")
        title = self.title()
        super().__init__(title, content)
        self.create(self.filename)

    def title(self):
        tag = self.soup.find("h1")
        if tag:
            return tag.text


class About(Page):
    def __init__(self):
        self.title = "درباره من"
        self.content = File.read("components/about.html")
        self.filename = "about.html"
        super().__init__(self.title, self.content)
        self.create(self.filename)


class Blog(Page):
    def __init__(self):
        self.title = "Blog | بلاگ"
        self.filename = "blog.html"
        article = Article(self.filename)
        articles = article.all()
        content = article.join(articles)
        super().__init__(self.title, content)
        self.create(self.filename)


class Index(Page):
    title = "سعید غلامی | Saeed Gholami"
    filename = "index.html"

    def __init__(self):
        intro = Intro("intro.html")
        article = Article("recent_posts.html")
        articles = article.get(number=3)
        recent_articles = article.join(articles)
        template = File.read("./components/recent_posts.html")
        kw = {"recent_articles": recent_articles}
        recent_articles = template.format(**kw)
        content = f"{intro.html}\n{recent_articles}"

        super().__init__(self.title, content)
        if os.path.exists(self.filename):
            os.remove(self.filename)

        self.create(self.filename)
        shutil.move(f"./pages/{self.filename}", "./")


post = Post("post_001.md")


# class Template:
#     PATH = File.BASE_DIR / "templates"
#
#     @classmethod
#     def build(cls, template, **kw):
#         return template.format(**kw)
#
#
# class Component:
#     def __init__(self):
#         pass
#
#
# class Page:
#     PATH = File.BASE_DIR / "pages"
#
#     def __init__(self, title: str, content: str):
#         self.title = title
#         self.content = content
#         self.build()
#
#     def build(self):
#         base = File.read("./templates/base.html")
#         nav = File.read("./includes/nav.html")
#         footer = File.read("./includes/footer.html")
#         kw = {
#             "title": self.title,
#             "nav": nav,
#             "content": self.content,
#             "footer": footer,
#         }
#         self.content = Template.build(base, **kw)
#
#     def create(self, filename):
#         File.write(filename, self.content)
#
#
# class Post:
#     def __init__(self, filename):
#         self.filename = filename
#         md = File.read(self.filename)
#         self.html = self.md_to_html(md)
#         self.soup = BeautifulSoup(self.html, "html.parser")
#
#     @classmethod
#     def post_files(cls, number=-1):
#         files = os.listdir("./posts/")
#         post_files = sorted([file for file in files], reverse=True)
#         if number > 0:
#             return post_files[:number]
#         return post_files
#
#     def build(self):
#         html_filename = self.filename.replace(".md", ".html")
#         page = Page(self.filename, self.html)
#         page.build()
#         page.create(html_filename)
#
#     @classmethod
#     def create_all(cls):
#         post_files = os.listdir("./posts")
#         for post_file in post_files:
#             post = File.read(f"./posts/{post_file}")
#             html = markdown.markdown(post)
#             page = Page("title", html)
#             html_filename = post_file.replace(".md", ".html")
#             page.create(f"./pages/{html_filename}")
#
#     def md_to_html(self, filename):
#         return markdown.markdown(filename)
#
#     def get_tag_by_name(self, name):
#         tag = self.soup.find(name)
#         if isinstance(tag, bs4.element.Tag):
#             return tag
#
#     def title(self):
#         tag = self.get_tag_by_name("h1")
#         if tag:
#             return tag.text
#         return "post title not found"
#
#     def summary(self):
#         tag = self.get_tag_by_name("p")
#         if tag:
#             return tag.text
#         return "post summary not found"
#
#     def post_info(self):
#         tag = self.soup.find(id="post-info")
#         if tag:
#             return tag.text
#         return "post info not found"
#
#
# class Blog:
#     def post_list(self):
#         posts = []
#         # make sure all markdown files converted to html
#         Post.create_all()
#         files = os.listdir("./pages")
#         post_files = [file for file in files if file.startswith("post_")]
#         for post_file in post_files:
#             html = File.read(f"./pages/{post_file}")
#             soup = BeautifulSoup(html, "html.parser")
#             title = soup.find("h1")
#             summary = soup.find("p")
#             post_part = File.read("./templates/post_part.html")
#             kw = {
#                 "post_title": title,
#                 "post_summary": summary,
#                 "date": "2020/2/12",
#                 "mins": "3 mins",
#                 "tag": "python",
#             }
#             post = Template.build(post_part, **kw)
#             posts.append(post)
#
#         post_row = "\n".join(posts)
#         kw = {"recent_posts": post_row}
#         blog_page = Template.build(post_row, **kw)
#         page = Page("blog", blog_page)
#         print(post_row)
#         # page.create("blog.html")
#
#
# class Index:
#     TITLE = "Saeed Gholami | سعید غلامی"
#     FILENAME = "index.html"
#     PATH = os.path.join("main", FILENAME)
#     CONTENT = File.read(PATH)
#
#     @classmethod
#     def build(cls):
#         content = cls.recent_posts()
#         page = Page(cls.TITLE, content)
#         page.create(cls.FILENAME)
#
#     @classmethod
#     def recent_posts(cls):
#         """add 3 most recent posts in the index page."""
#         posts = []
#         post_files = Post.post_files(3)
#         for post_file in post_files:
#             post = Post(f"./posts/{post_file}")
#             title = post.title()
#             summary = post.summary()
#             post_part = File.read("./templates/post_part.html")
#             kw = {
#                 "post_title": title,
#                 "post_summary": summary,
#                 "date": "2020/2/12",
#                 "mins": "3 mins",
#                 "tag": "python",
#             }
#             post = Template.build(post_part, **kw)
#             posts.append(post)
#         recent_posts = "\n".join(posts)
#         kw = {"recent_posts": recent_posts}
#         index = Template.build(cls.CONTENT, **kw)
#         return index


# class Command:
#     @classmethod
#     def update(cls):
#         """update neccessary parts."""
#         # post = Post("./posts/post_001.md")
#         # post.build()
#         # Post.create_all()
#         # Index.recent_posts()
#         # Index.build()
#         blog = Blog()
#         blog.post_list()
#
#     @classmethod
#     def build(cls):
#         """build everything from scratch."""
#         pass
#
#     @classmethod
#     def publish(cls):
#         """publish to github page."""
#         pass
#
#
# def main():
#     if len(sys.argv) < 2:
#         print("Usage: sgo [<update>, <publish>]")
#         return
#
#     if sys.argv[1] == "update":
#         Command.update()
#     elif sys.argv[1] == "publish":
#         Command.publish()
#     else:
#         print("Unknown operation.")
#
#
# if __name__ == "__main__":
#     main()
