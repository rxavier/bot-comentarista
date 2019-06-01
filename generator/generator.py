import markovify
import json
from crawlers import el_pais


def make_model():

    el_pais.get_comments()

    with open("../crawlers/comments.txt", "r") as txt:
        comments_text = txt.read()

    model = markovify.NewlineText(comments_text)

    model_json = model.to_json()
    with open("../generator/model.json", "w") as f:
        json.dump(model_json, f)

    return model
