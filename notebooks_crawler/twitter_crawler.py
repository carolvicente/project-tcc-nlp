from personas_sources.political_liders import read_liders
from helpers.api_monitor import request_time_missing_to_reset, request_quantity_remaining
from helpers.api_query import build_tweet_api_query
from helpers.credentials import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
from twython import Twython
import csv
import json
import pandas as pd
import time
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))


twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                  ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

API_STANDARD_REQUEST_QTY = 180
API_INTERVAL_REQUESTS = 15*60
tweets_persona = []


def monitoring_quantity_routine():
    res = request_quantity_remaining(twitter)
    print(res)
    while type(res) == str:
        time.sleep(2*60)
        res = request_quantity_remaining(twitter)
    return 1


def routine_search(requests_per_persona, lst_persona, twitter, search_qty):

    # monitoring_quantity_routine()
    for q in range(search_qty):
        for l in lst_persona:
            print('#### READING {} ####'.format(l.name))
            search_tweet(l)
    # time.sleep(API_INTERVAL_REQUESTS)


def search_tweet(persona):
    query = persona.twitter_query
    print(query)
    res = twitter.search(q=query, count='5',
                         lang='pt', tweet_mode='extended', since_id=persona.since_id)

    # res = twitter.cursor(twitter.search,
    #                      q=query,
    #                      since_id=persona.since_id,
    #                      count='5',
    #                      lang='pt',
    #                      tweet_mode='extended')

    # print(res)
    # print('#########=======#########')
    # for result in res:
    #     print(result)
    #     text = ''
    #     if 'retweeted_status' in dir(result):
    #         text = result.retweeted_status.full_text
    #         print('#### Text :', text)
    #     else:
    #         try:
    #             text = result.full_text
    #             print('#### FULL TEXT :', text)
    #         except Exception:
    #             print('JSON Malformado.')
    #     if len(text) > 0:
    #         tweets_persona.append({'persona': persona.name, 'tweet': text})

# max_id = res['search_metadata']['max_id']
# since_id = res['search_metadata']['since_id']

#persona.since_id = since_id

# for result in res['statuses']:
#     if 'retweeted_status' in result:
#         text = result['retweeted_status']['full_text']
#         print('#### Text :', text)
#     else:
#         text = result['full_text']
#         print('#### Text :', text)
#     tweets_persona.append({'persona': persona.name, 'tweet': text})


def main():

    lst_persona, df_persona = read_liders()

    personas_qty = len(lst_persona)
    requests_per_persona = int(API_STANDARD_REQUEST_QTY/personas_qty)

    routine_search(5, lst_persona, twitter, 1)
    df_tweets = pd.DataFrame(tweets_persona)

    for l in lst_persona:
        df_persona.loc[l.name, 'twitter_since_id'] = l.since_id

    # df_tweets.to_csv('../datasets/twitter/tweets_data.csv',
    #                  sep=',', encoding='utf-8')

    # df_persona.to_csv('../datasets/twitter/political_liders.csv',
    #                   sep=',', encoding='utf-8')

    # with open('../datasets/twitter/tweets_data.csv', 'a') as csvFile:
    #     writer = csv.writer(csvFile)
    #     for index, row in df_tweets.iterrows():
    #         writer.writerow(row)
    # csvFile.close()

    # with open('../datasets/twitter/political_liders.csv', 'a') as csvFile:
    #     writer = csv.writer(csvFile)
    #     for index, row in df_persona.iterrows():
    #         writer.writerow(row)
    # csvFile.close()


if __name__ == '__main__':
    main()
