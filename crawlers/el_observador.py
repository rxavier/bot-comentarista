import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

BASE_URL = "https://www.elobservador.com.uy"
URL = "https://www.elobservador.com.uy/elobservador/nacional"

response = requests.get(URL).text
response_soup = BeautifulSoup(response, "lxml")

items = response_soup.find_all("a", href=re.compile("/nota/"))

article_links = []
for item in items:
    article_links.append(BASE_URL + item["href"])

article_links = list(set(article_links))

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

raw_comments = []
for article in article_links:
    article_response = driver.get(article)
    time.sleep(3)
    article_html = driver.page_source
    article_soup = BeautifulSoup(article_html, "lxml")
    article_comments = article_soup.find_all("div", class_="frison_text")

    for comment in article_comments:
        raw_comments.append(comment.get_text().strip())
