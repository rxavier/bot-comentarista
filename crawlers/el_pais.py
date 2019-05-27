import requests
import re
from bs4 import BeautifulSoup

base_url = "https://www.elpais.com.uy"
info_url = "https://www.elpais.com.uy/page/listado-informacion.html?page="
base_comment_url = "https://www.elpais.com.uy/comment/threads/article-"

username = "user"
password = "pass"

spam = "Este comentario se ha marcado como spam."


def get_comments():

    article_links = []
    for page in range(1, 11):
        info_response = requests.get(info_url + str(page)).text
        info_soup = BeautifulSoup(info_response, features="html.parser")

        page_links = info_soup.find_all("a", {'class': 'page-link', 'href': True})

        for link in page_links:
            article_links.append(base_url + link["href"])

    article_links = list(set(article_links))

    try:
        with open("../crawlers/article_links.txt", "r") as txt:
            previous_links = txt.read().splitlines()
    except IOError:
        previous_links = []

    unique_links = list(set(article_links) - set(previous_links))

    with open("../crawlers/article_links.txt", "a+") as txt:
        for link in unique_links:
            txt.write("%s\n" % link)

    previous_links.extend(unique_links)

    comments = []
    with requests.Session() as session:
        session.post("https://sso.elpais.com.uy/cas/login", data={"username": username, "password": password})

        for article in unique_links:
            article_response = session.get(article).text
            article_soup = BeautifulSoup(article_response, features="html.parser")
            article_id = article_soup.find("meta", {"name": "cXenseParse:recs:articleid"})["content"]

            comments_url = base_comment_url + article_id + "/comments"

            comments_response = session.get(comments_url).text
            comments_soup = BeautifulSoup(comments_response, features="html.parser")
            comments_find = comments_soup.find_all("div", {"class": "comment-text"})

            for comment in comments_find:

                comment_1 = re.sub("\r", "", comment.get_text().strip())

                if comment_1 != spam:
                    comment_2 = re.sub("\n+", ". ", comment_1)
                    comment_3 = re.sub(r'\s([?.!"](?:\s|$))', r'\1', comment_2)

                    if re.search("[.!?\\-]", comment_3[-1]) is None:
                        comment_parse = comment_3 + "."
                    else:
                        comment_parse = comment_3

                    comments.append(comment_parse)

    with open("../crawlers/comments.txt", "a+") as txt:
        for comment in comments:
            txt.write("%s\n" % comment)

    return previous_links, comments
