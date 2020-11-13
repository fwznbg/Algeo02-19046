import requests
from bs4 import BeautifulSoup

# url to be scrapped
url = "https://techcrunch.com/2020/11/12/macos-apps-wont-launch/"
response = requests.get(url)

# get html content
soup = BeautifulSoup(response.content, "html.parser")

# get title
title = soup.findAll("h1", class_="article__title")
# get the content(paragraphs)
paragraphs = soup.findAll('div', class_="article-content")

# make new file and write the title to it
f = open("./static/simplesearchengine/{}.txt".format(title[0].text.split(":")[0]), "x")
for x in title:
    f.write(x.get_text())
f.close()

with open("./static/simplesearchengine/{}.txt".format(title[0].text.split(":")[0]), "a", encoding="utf-8") as f:
    for x in paragraphs:
        f.write(x.text)
