import requests
import re
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

                comment_process_1 = re.sub("\r", "", comment.get_text().strip())

                if comment_process_1 != spam:
                    """Replace newlines with period and space"""
                    comment_process = re.sub("\n+", ".", comment_process_1)
                    """Add space after any punctuation if missing"""
                    comment_process = re.sub("(?<=[?.!:,;])(?=[^\\s])(?![.!?/0-9]|com|org|net|gub|edu|uy|blogspot)",
                                             " ", comment_process)
                    """Remove space before punctuation"""
                    comment_process = re.sub(r'\s([?.!,;]+(?:\s|$))', r'\1', comment_process)
                    """Remove period following any kind of punctuation"""
                    comment_process = re.sub("(?<=[?!¿¡,;])\\.(?![.])", "", comment_process)
                    """Add space after ellipsis if missing"""
                    comment_process = re.sub("\\.{2-3}(?!\\s)", "... ", comment_process)

                    """End string with period if not available"""
                    if re.search("[.!:?\\-]", comment_process[-1]) is None:
                        comment_process = comment_process + "."

                    parsed_comments.append(comment_process)
                    raw_comments.append(comment_process_1)

    if save is True:
        with open("../crawlers/comments.txt", "a+") as txt:
            for comment in parsed_comments:
                txt.write("%s\n" % comment)

    return previous_links, parsed_comments, raw_comments
