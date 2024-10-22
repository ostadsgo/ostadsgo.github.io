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


class Template:
    PATH = File.BASE_DIR / "templates"

    def __init__(self, filename):
        self.template = File.read(str(self.PATH / filename))
        self.html = self.template

    def render(self, data):
        self.html = self.template.format(**data)
        return self.html


class Article(Template):
    """Extract article form a post."""

    def __init__(self, post_name):
        filename = "post_article.html"
        super().__init__(filename)
        # extrac data from post_name
        md = File.read(f"./posts/{post_name}")
        html = markdown.markdown(md)
        self.soup = BeautifulSoup(html, "html.parser")

        date, mins, tag = self.info()
        post_link = f"/pages/{post_name.replace('.md', '.html')}"
        print(post_link)
        data = {
            "post_link": post_link,
            "post_title": self.title(),
            "date": date.strip(),
            "mins": mins.strip(),
            "tag": tag.strip(),
            "post_summary": self.summary(),
        }
        self.render(data)

    def title(self):
        tag = self.soup.find("h1")
        if tag:
            return tag.text
        return "Title of the post not found!"

    def info(self):
        tag = self.soup.find_all("p")
        if tag:
            return tag[0].text.split("  ")
        return "Summary of the post not  found!"

    def summary(self):
        tag = self.soup.find_all("p")
        if tag:
            return tag[1].text
        return "Summary of the post not  found!"


class Page:
    def __init__(self, title, content):
        self.title = title
        self.nav = Template("nav.html")
        self.footer = Template("footer.html")
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

    @classmethod
    def get(cls, number=3):
        articles = []
        files = sorted(os.listdir("./posts"), reverse=True)
        recent_files = files[:number]
        for file in recent_files:
            article = Article(file)
            articles.append(article.html)

        return "\n".join(articles)


class About(Page):
    def __init__(self):
        self.title = "درباره من"
        self.filename = "about.html"
        self.content = Template(self.filename).html
        super().__init__(self.title, self.content)
        self.create(self.filename)


class Blog(Page):
    def __init__(self):
        self.title = "Blog | بلاگ"
        self.filename = "blog.html"
        template = Template("blog.html")
        data = {"articles": Post.get(100)}
        content = template.render(data)
        super().__init__(self.title, content)
        self.create(self.filename)


class Index(Page):
    def __init__(self):
        title = "سعید غلامی | Saeed Gholami"
        filename = "index.html"
        intro = Template("intro.html").html
        # Recent Posts
        recent_template = Template("recent_posts.html")
        recent_posts = recent_template.render({"articles": Post.get(3)})
        # Index
        template = Template("index.html")
        data = {"intro": intro, "articles": recent_posts}
        content = template.render(data)
        super().__init__(title, content)

        if os.path.exists(filename):
            os.remove(filename)

        self.create(filename)
        shutil.move(f"./pages/{filename}", "./")


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
        """build  only dynamic parts .
        build only markdown that recently created
        update index recent articles and blog page."""
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
