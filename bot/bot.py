import tweepy
from generator import generator

consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_token = "access_token"
access_token_secret = "access_token_secret"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def make_tweet():
    tweet = generator.get_tweet(new=False)
    api.update_status(tweet)
