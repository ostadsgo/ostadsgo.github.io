#! /uelsr/bin/python


import os
import shutil
import sys
from pathlib import Path

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


class Article(Component):
    def __init__(self, html_file):
        super().__init__(html_file)
        self.title = "post title"
        self.summary = "post summary"
        self.articles = []
        self.make()

    def make(self):
        post_files = sorted(os.listdir("./posts"), reverse=True)
        for post_file in post_files:
            md = File.read(f"./posts/{post_file}")
            html = markdown.markdown(md)
            soup = BeautifulSoup(html, "html.parser")
            post_title_tag = soup.find("h1")
            p_tags = soup.find_all("p", limit=2)
            post_info = p_tags[0]
            post_summary_tag = p_tags[1]
            if post_title_tag:
                self.title = post_title_tag.text
            self.summary = post_summary_tag.text
            post_date, post_mins, post_tag = post_info.text.split("  ")
            post_file_html = post_file.replace(".md", ".html")
            kw = {
                "post_title": self.title,
                "post_link": f"/pages/{post_file_html}",
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

    @classmethod
    def all(cls):
        files = os.listdir("./posts")
        for file in files:
            md = File.read(f"./posts/{file}")
            content = markdown.markdown(md)
            soup = BeautifulSoup(content, "html.parser")
            title_tag = soup.find("h1")
            title = "Uknown"
            if title_tag:
                title = title_tag.text
            page = Page(title, content)
            filename = file.replace(".md", ".html")
            page.create(filename)


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
        intro = Component("intro.html")
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


class Command:
    @classmethod
    def build(cls):
        Index()
        About()
        Blog()
        Post.all()
        print("Build all pages.")

    @classmethod
    def update(cls):
        """update index recent articles and blog page."""
        pass

    @classmethod
    def publish(cls):
        os.system("git add -A")
        os.system("git commit -m 'Update and publish'")
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
