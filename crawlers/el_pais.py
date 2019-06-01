import requests
import re
from crawlers import text_parser
from bs4 import BeautifulSoup

base_url = "https://www.elpais.com.uy"
info_url = "https://www.elpais.com.uy/page/listado-informacion.html?page="
base_comment_url = "https://www.elpais.com.uy/comment/threads/article-"

username = "user"
password = "pass"

spam = "Este comentario se ha marcado como spam."


def get_comments(save=True):

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

    raw_comments = []
    parsed_comments = []
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

                raw = re.sub("\r", "", comment.get_text().strip())

                if raw != spam:
                    processed = text_parser.sanitizer(raw)

                    parsed_comments.append(processed)
                    raw_comments.append(raw)

    if save is True:
        with open("../crawlers/comments.txt", "a+") as txt:
            for comment in parsed_comments:
                txt.write("%s\n" % comment)

    return previous_links, parsed_comments, raw_comments
