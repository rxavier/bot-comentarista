import tweepy
import markovify
import json
import time
from generator import generator

consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_token = "access_token"
access_token_secret = "access_token_secret"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

handle = api.me().screen_name


def make_tweet(update_model=False, update_status=True):

    if update_model is True:
        model = generator.make_model()

    else:
        with open("../generator/model.json", "r") as f:
            model_json = json.load(f)
        model = markovify.NewlineText.from_json(model_json)

    tweet = model.make_short_sentence(280)

    if update_status is True:
        api.update_status(tweet)
        print(f"Tweeted {tweet}")

    return tweet


def fulfill_request(hashtag="generar"):

    last_reply_id = None
    for status in tweepy.Cursor(api.home_timeline).items(50):
        if status.in_reply_to_status_id is not None:
            last_reply_id = status.in_reply_to_status_id
            break
        else:
            pass

    if last_reply_id is not None:
        cursor = tweepy.Cursor(api.search, q=f"@{handle} -filter:retweets + #{hashtag}",
                               since_id=last_reply_id).items(50)
    else:
        cursor = tweepy.Cursor(api.search, q=f"@{handle} -filter:retweets + #{hashtag}").items(50)

    for reply in cursor:

        request_reply = make_tweet(update_model=False, update_status=False)
        api.update_status(request_reply, in_reply_to_status_id=reply.id, auto_populate_reply_metadata=True)
        time.sleep(10)
