# bot.py
# heavily drawn from waleadesina @ https://scotch.io/tutorials/build-a-tweet-bot-with-python#toc-storing-credentials

import tweepy
from secrets import *
from sentiment_analysis import avg_sentiment
import numpy as np
from datetime import datetime
import json
from meme_machine import MemeMachine
import requests
import os


class TwitterBot:

    def __init__(self):
        # create an OAuthHandler instance
        # Twitter requires all requests to use OAuth for authentication
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        self.auth.set_access_token(access_token, access_secret)

        # Construct the API instance
        self.api = tweepy.API(self.auth)  # create an API object

        self.memebot = MemeMachine()

        self.users = self.get_users_from_json()

    # A function to tweet at users that have just followed the bot. Tailor to give responses
    # based on how happy the person is. Consider abstracting that to checkHappiness.
    # Consider giving resources at the end of introductory message plus a wholesome picture.
    def follower_message(self):
        for user in tweepy.Cursor(self.api.followers).items():
            UID = user.id_str
            tweets = self.api.user_timeline(user_id=UID, count=100)
            gap = self.tweet_time(tweets)
            status = self.check_happiness(UID, tweets, gap)
            username = user.screen_name
            message = "Hi " + username + " " + status
            self.api.send_direct_message(user_id=UID, text=message)

    # check largest gap of time between last 100 tweets
    def tweet_time(self, tweets):
        longest = 0
        if len(tweets) > 1:
            length = 5
            if len(tweets) < length:
                length = len(tweets)
            d1 = tweets[0].created_at
            for i in np.arange(1, length, 1):
                d0 = d1
                d1 = tweets[i].created_at
                templongest = abs(d1 - d0).total_seconds() / 3600
                if templongest > longest:
                    longest = templongest
        return longest


    # A tweet to check in
    def wholesome_tweet(self):
        url = self.memebot.get_meme()
        message = "we wish you a merry February"
        filename = 'temp.jpg'
        request = requests.get(url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            self.api.update_with_media(filename, status=message)
            os.remove(filename)
        else:
            print("Unable to download image")

    # happiness check function
    def check_happiness(self, UID, tweets, gap):
        statuses = tweets
        tweets = [st.text for st in statuses]
        senti = avg_sentiment(tweets)['compound']
        message = ""
        if gap < .20:
            message = "you've been on twitter a lot! Take a break and get some fresh air! Also"
        if senti > 0.10:
            message += " it looks like you're doing well!"
        elif senti < -0.10:
            message += " it seems like you're a little bit blue. :( Maybe you could reach out to a friend?"
        else:
            message += " it seems like you're so-so.. Maybe it's time to take a nice walk?"
        return message

    def get_users_from_json(self):
        with open('users.json', 'r') as f:
            datastore = json.load(f)
        return datastore

    def update_json(self, unfollowed_users, new_users):
        if new_users or unfollowed_users:
            for user1 in new_users:
                self.users[user1] = 0
                print("in loop1")
            for user2 in unfollowed_users:
                del self.users[user2]
                print("in loop2")
            with open('users.json', 'w') as outfile:
                json.dump(self.users, outfile)


    def send_message_to_new_users(self):
        pulled_users = set(self.api.followers_ids())
        users = set(int(n) for n in self.users.keys())
        new_users = pulled_users - users
        unfollowed_users = users - pulled_users
        self.update_json(unfollowed_users, new_users)

        for user in new_users:
            username = self.api.get_user(str(user)).screen_name
            message = "Hi " + username + ", I'm Happy Bot."
            self.api.send_direct_message(user_id=str(user), text=message)

