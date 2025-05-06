import markdown

from pygments.formatters import HtmlFormatter

# Generate CSS
formatter = HtmlFormatter(style='github-dark')
with open('pygments.css', 'w') as f:
    f.write(formatter.get_style_defs('.codehilite'))

md = ""
with open("test.md") as f:
    md = f.read()

html = markdown.markdown(md, extensions=['fenced_code', 'codehilite'])

with open("test.html", "w") as f:
    f.write(html)






