import tweepy
import markovify
import json
from generator import generator

consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_token = "access_token"
access_token_secret = "access_token_secret"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def make_tweet(new=False):

    if new is True:
        model = generator.make_model()

    else:
        with open("../generator/model.json", "r") as f:
            model_json = json.load(f)
        model = markovify.NewlineText.from_json(model_json)

    tweet = model.make_short_sentence(280)

    api.update_status(tweet)
    print("Tweeted: " + tweet)
