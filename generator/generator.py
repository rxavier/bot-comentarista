import markovify
import json
from crawlers import el_pais


def get_tweet(sentences=1, new=True, tweet=True):

    if new is True:
        articles, comments_text = el_pais.get_comments()
        model = markovify.Text(comments_text)

        model_json = model.to_json()
        with open("model.json", "w") as f:
            json.dump(model_json, f)

    else:
        with open("model.json", "r") as f:
            model_json = json.load(f)
        model = markovify.Text.from_json(model_json)

    if sentences > 1:

        output = []
        for i in range(sentences):

            if tweet is True:
                output.append(model.make_short_sentence(280))
            else:
                output.append(model.make_sentence())

    else:

        if tweet is True:
            output = model.make_short_sentence(280)
        else:
            output = model.make_sentence()

    return output
