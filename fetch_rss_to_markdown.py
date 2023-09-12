import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime


def fetch_rss_to_markdown():
    with urllib.request.urlopen("https://matt-rickard.com/rss") as response:
        rss = ET.fromstring(response.read())
    return "\n\n".join(
        [
            f"{datetime.strptime(item.find('pubDate').text, '%a, %d %b %Y %H:%M:%S %Z').strftime('`%m-%d`')} [{item.find('title').text}]({item.find('link').text})"
            for item in rss.findall(".//item")
        ]
    )

def update_readme(blog_links):
    with open("README.md", "r") as f:
        lines = f.readlines()
    
    start_idx, end_idx = None, None
    
    for i, line in enumerate(lines):
        if "<!--- start_blog -->" in line:
            start_idx = i
        if "<!--- end_blog -->" in line:
            end_idx = i
    
    if start_idx is not None and end_idx is not None:
        new_lines = lines[:start_idx+1] + [blog_links + "\n"] + lines[end_idx:]
        with open("README.md", "w") as f:
            f.write("".join(new_lines))

if __name__ == "__main__":
    blog_links = fetch_rss_to_markdown()
    update_readme(blog_links)
