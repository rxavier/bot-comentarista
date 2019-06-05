import tweepy
import markovify
import json
import os

consumer_key = os.environ["consumer_key"]
consumer_secret = os.environ["consumer_secret"]
access_token = os.environ["access_token"]
access_token_secret = os.environ["access_token_secret"]
json_path = os.environ['LAMBDA_TASK_ROOT'] + "/model.json"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def make_tweet(update_status=True):

    with open(json_path, "r") as f:
        model_json = json.load(f)
    model = markovify.NewlineText.from_json(model_json)

    tweet = model.make_short_sentence(280)

    if update_status is True:
        api.update_status(tweet)
        print(f"Tweeted: {tweet}")

    return tweet


def lambda_handler(event, context):

    make_tweet()
