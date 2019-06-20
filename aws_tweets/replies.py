import tweepy
import markovify
import json
import os
import time

consumer_key = os.environ["consumer_key"]
consumer_secret = os.environ["consumer_secret"]
access_token = os.environ["access_token"]
access_token_secret = os.environ["access_token_secret"]
json_path = os.environ['LAMBDA_TASK_ROOT'] + "/model.json"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

handle = api.me().screen_name


def make_tweet(update_status=True):

    with open(json_path, "r") as f:
        model_json = json.load(f)
    model = markovify.NewlineText.from_json(model_json)

    tweet = model.make_short_sentence(280)

    if update_status is True:
        api.update_status(tweet)
        print(f"Tweeted {tweet}")

    return tweet


def fulfill_request(search_term="#focatweet OR #focatuit"):

    past_replies = []
    for status in tweepy.Cursor(api.home_timeline).items(50):
        if status.in_reply_to_status_id is not None:
            past_replies.append(status.in_reply_to_status_id)
        else:
            pass

    try:
        last_reply_id = past_replies[0]
        cursor = tweepy.Cursor(api.search, q=f"{search_term} -filter:retweets",
                               since_id=last_reply_id).items(50)
    except IndexError:
        cursor = tweepy.Cursor(api.search, q=f"{search_term} -filter:retweets").items(50)

    replied_users = []
    for request in cursor:

        if request.id not in past_replies:
            request_reply = make_tweet(update_status=False)
            api.update_status(request_reply, in_reply_to_status_id=request.id, auto_populate_reply_metadata=True)
            replied_users.append(request.user.screen_name)
            time.sleep(3)

    return replied_users


def lambda_handler(event, context):

    replies = fulfill_request()

    print("Replied to:")
    print(*replies, sep="\n")
