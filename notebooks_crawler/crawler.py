from helpers.credentials import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
from helpers.api_query import build_tweet_api_query
from helpers.api_monitor import request_time_missing_to_reset, request_quantity_remaining
from personas_sources.political_liders import read_liders
import tweepy
import csv
import pandas as pd
import json
import time
from datetime import datetime
import calendar
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))


API_STANDARD_REQUEST_QTY = 180
API_INTERVAL_REQUESTS = 15*60


consumer_key = 'QrUJ9qYjRgrZpYN5Y9HmdEAE0'
consumer_secret = 'TUxMWiFro9XTCNu4P8gEGvHiar2vv29TGCrjckIaDtZnGtjHcz'
access_token = '1489245714-RQh3ihkf1FgRjRYPFF6sSRpIUW2LuLxEARD7ylj'
access_token_secret = 'nLcMAXRX0z2PIUmuEApEU4nj5KWdLymno1aHPLyTWBFVG'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

count = 0


def epoch_to_minutes(epoch):
    a = int(epoch)
    b = int(time.time())  # current epoch time
    c = a - b  # returns seconds
    minutes = c // 60 % 60
    print(minutes)
    return minutes


def request_tweets_remaining():
    data = api.rate_limit_status()
    remaining = data['resources']['application']['/application/rate_limit_status']['remaining']
    print(remaining)
    return remaining


def request_time_remaining():
    data = api.rate_limit_status()
    epoch = data['resources']['application']['/application/rate_limit_status']['reset']
    limit = data['resources']['application']['/application/rate_limit_status']['limit']
    return epoch_to_minutes(epoch)


def tweets_to_csv(lst_all_tweets):
    csvFile = open('ua.csv', 'a')
    csvWriter = csv.writer(csvFile)
    for tweet in lst_all_tweets:
        csvWriter.writerow([tweet])


def search_with_no_since_id(persona, lst_all_tweets):
    query = persona.twitter_query
    since_id = persona.since_id
    last_since_id = persona.since_id
    print(query)
    for tweet in tweepy.Cursor(api.search, q=query, rpp=2,
                               lang="pt", tweet_mode='extended').items():
        text = ''
        if tweet.retweeted is 'False':
            text = tweet.text
        else:
            text = tweet.full_text
        lst_all_tweets.append([persona.name, text])
        last_since_id = tweet.id

    persona.since_id = last_since_id


def search_with_since_id(persona, lst_all_tweets):
    query = persona.twitter_query
    since_id = persona.since_id
    last_since_id = persona.since_id
    print(query)
    for tweet in tweepy.Cursor(api.search, q=query, rpp=2,
                               lang="pt", since_id=since_id, tweet_mode='extended').items():
        text = ''
        if tweet.retweeted is 'False':
            text = tweet.text
        else:
            text = tweet.full_text
        lst_all_tweets.append([persona.name, text])
        last_since_id = tweet.id
    persona.since_id = last_since_id


def search_tweet(persona, lst_all_tweets):
    search_with_since_id(persona, lst_all_tweets)


def main():
    lst_persona, df_persona = read_liders()

    personas_qty = len(lst_persona)
    requests_per_persona = int(API_STANDARD_REQUEST_QTY/personas_qty)
    lst_all_tweets = []

    if request_tweets_remaining() <= 0:
        minutes_missing_call = request_time_remaining()
        while minutes_missing_call > 0:
            time.sleep(1)
            minutes_missing_call = request_time_remaining()

    for l in lst_persona:
        print(l.name, l.since_id)
        print('Before', l.since_id)
        search_tweet(l, lst_all_tweets)
        print('After', l.since_id)

        for l in lst_all_tweets:
            print(l)

        # tweets_to_csv(lst_all_tweets)

        # for l in lst_persona:
        #     df_persona.loc[l.name, 'twitter_since_id'] = l.since_id

        # df_persona.to_csv('personas_sources/political_liders.csv',
        #                   sep=',', encoding='utf-8')

        # # with open('../datasets/twitter/political_liders.csv', 'a') as csvFile:
        # #     writer = csv.writer(csvFile)
        # #     for index, row in df_persona.iterrows():
        # #         writer.writerow(row)
        # #     csvFile.close()


if __name__ == '__main__':
    main()
