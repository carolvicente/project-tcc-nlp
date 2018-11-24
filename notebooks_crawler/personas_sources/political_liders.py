import csv
import pandas as pd


class Lider:
    def __init__(self, name, party, popular_names, twitter_query, max_id, since_id, file):
        self.name = name
        self.party = party
        self.popular_names = popular_names
        self.twitter_query = twitter_query
        self.max_id = max_id
        self.since_id = since_id
        self.file = file


def read_liders():

    lst_liders = list()
    dt_liders = pd.read_csv('personas_sources/political_liders.csv')
    dt_liders.set_index('Name', inplace=True)

    for index, row in dt_liders.iterrows():
        name = index
        party = row['Party_name']
        popular_names = row['popular_names']
        file = row['file']
        twitter_query = row['twitter_query']
        max_id = row['twitter_max_id']
        since_id = row['twitter_since_id']
        lider = Lider(name, party, popular_names,
                      twitter_query, max_id, since_id, file)
        lst_liders.append(lider)

    return lst_liders, dt_liders


if __name__ == '__main__':
    read_liders()
