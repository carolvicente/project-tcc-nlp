from bs4 import BeautifulSoup
from personas_sources.political_liders import read_liders
import csv
import requests
import os
import sys
sys.path.insert(0, os.path.abspath("../"))
dir_path = os.path.dirname(os.path.realpath(__file__))

URL = 'https://brasil.elpais.com/seccion/politica/'
PAGE_NUMBER = 170


class ElPaisNew:
    def __init__(self, title, description, url, date, page):
        self.title = title
        self.description = description
        self.url = url
        self.date = date
        self.page = page


class LiderNews:
    def __init__(self, name, popular_names, file):
        self.name = name
        self.popular_names = popular_names
        self.file = file


class Article:
    def __init__(self, title, description, popular_names, name, file, date):
        self.title = title
        self.description = description
        self.name = name
        self.popular_names = popular_names
        self.date = date
        self.file = file
        self.text = list()

    def create_text(self, paragraph):
        self.text.append(paragraph)


def last_recorded_date():
    ifile = open('../datasets/el_pais/el_pais_post.csv', "rt")
    read = csv.reader(ifile)
    firstline = True
    last_new_date = 0
    page_num = 0
    for row in read:
        if firstline is False:
            last_new_date = row[0]
            page_num = row[1]
            break
        firstline = False
    return last_new_date, page_num


def get_news_info(news_feed, news_feed_list, current_page):

    for n in news_feed:
        date = ''
        url = ''
        title = ''
        description = ''
        try:
            date = n.div.time['datetime']
            url = str(n.div.h2.a['href']).replace('//', 'https://')
        except:
            pass
        try:
            title = n.div.h2.a.text
            description = n.div.p.text
        except:
            pass
        if title == '' or description == '' or url == '':
            continue
        new = ElPaisNew(title, description, url, date, current_page)
        news_feed_list.append(new)

    return news_feed_list


def get_news_for_days(page_numbers, news_feed_list, last_post_date, last_post_page):

    for n in range(page_numbers):
        current_page = PAGE_NUMBER - n
        url = 'https://brasil.elpais.com/seccion/politica/{}'.format(
            str(current_page))
        if 'https:https://' in url:
            url = url.replace('https:https://', 'https://')
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        news_feed = soup.select_one(
            '#principal > section > div > div.articulos.articulos_cuerpo > div')

        if news_feed is not None:
            news_feed = news_feed.find_all('article')
            get_news_info(news_feed, news_feed_list, current_page)

        news_feed_below_section = soup.select_one(
            '#principal > section > div > div.articulos.articulos_cierre > div')

        if news_feed_below_section is not None:
            news_feed_below_section = news_feed_below_section.find_all(
                'article')
            get_news_info(news_feed_below_section,
                          news_feed_list, current_page)


def write_to_csv(news_feed_list):
    with open('../datasets/el_pais/el_pais_post.csv', 'w') as csvfile:
        fw = csv.writer(csvfile, delimiter=',')
        fw.writerow(['date', 'page', 'title', 'description', 'url'])
        for n in range(len(news_feed_list) - 1):
            description = '"{0}"'.format(news_feed_list[n].description)
            fw.writerow([news_feed_list[n].date, news_feed_list[n].page, news_feed_list[n].title,
                         description, news_feed_list[n].url])

    csvfile.close()


def get_news_by_liders(liders_list):
    ifile = open('../datasets/el_pais/el_pais_post2.csv', "rt")
    read = csv.reader(ifile)
    firstline = True
    count = 0
    actual = list()
    lider_news = list()
    all_news = list()

    for row in read:
        if firstline is False:
            date = row[0]
            title = row[2]
            description = row[3]

            actual = [Article(title, description, l.popular_names.lower().split('|'), l.name, l.file, date) for l in liders_list if any(
                pop_names in description or pop_names in title for pop_names in l.popular_names)]

            if len(actual) > 0:
                url = row[4]
                print(url)
                if 'https:https://' in url:
                    url = url.replace('https:https://', 'https://')
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                news_feed = soup.select('#cuerpo_noticia')
                if len(news_feed) > 0:
                    news_feed = news_feed[0].find_all('p')
                    for n in news_feed:
                        all_news.append(n.text)
                        # for a in actual:
                        #     # print(a.popular_names)
                        #     if any(name in n.text.lower() for name in a.popular_names):
                        #         print('Found.')
                        #         a.create_text(n.text)
                    # lider_news.append(actual)
            else:
                continue
        firstline = False
    return lider_news, all_news


def main():
    # Pega lista de lideres para realizar buscas
    liders_csv_list, liders_df = read_liders()

    # Pega data do ultimo post, e página do ultimo post
    # news_feed_list = list()
    # last_post_date, last_post_page = last_recorded_date()

    # last_post_page = PAGE_NUMBER if last_post_page == 0 else last_post_page

    # Pega titulo principal das ultimas noticias do tópico a se procurar
    # get_news_for_days(10, news_feed_list, last_post_date, last_post_date)

    # write_to_csv(news_feed_list)

    liders_list = [LiderNews(l.name, l.popular_names, l.file)
                   for l in liders_csv_list]

    news_by_liders, all_news = get_news_by_liders(liders_list)

    # for news in news_by_liders:
    #     for n in news:
    #         path = '../datasets/el_pais/{0}'.format(
    #             n.file.strip())
    #         with open(path, 'a') as f:
    #             writer1 = csv.writer(f, delimiter=',')
    #             article = '"{0}"'.format('|'.join(n.text))
    #             writer1.writerow(
    #                 [n.date, n.title, n.description, article])
    #         f.close()

    path = '../datasets/el_pais/all_news4.csv'
    with open(path, 'a') as f:
        writer1 = csv.writer(f, delimiter='|')
        for n in all_news:
            writer1.writerow(
                [n])
        f.close()


if __name__ == '__main__':
    main()
