# El País Twitter Bot

## What

This project implements a Twitter bot that uses Markov chains to create messages similar to El País Uruguay newspaper user comments. There's two main functions:

* A function that tweets a new message every hour.
* A function that checks whether the bot has been mentioned with a specific hashtags and replies with a new message.

## Why

Basically because I expected it to have hilarious results due to the data the Markov chain is using. El País users are generally highly polarized right-wingers who have created some of the most creative insults for government officials.

## How

* The project uses [markovify](https://github.com/jsvine/markovify) for creating the messages and [tweepy](https://www.tweepy.org/) in order to interact with the Twitter API.
* Comments have been scraped from the [main El País news section](https://www.elpais.com.uy/informacion). At the moment of writing there's roughly 2500 comments.
* Because raw comments are fairly disorginzed, I sanitize them with very rough regex to fix punctuation.
* I use AWS Lambda to schedule one tweet per hour and reply to requests every 15 minutes.
