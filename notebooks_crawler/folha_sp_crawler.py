from bs4 import BeautifulSoup
import csv
import requests
import os
import sys
sys.path.insert(0, os.path.abspath("../"))


def get_full_news(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    full_text = ''
    print(url)

    content = soup.find(
        'div', attrs={'class': 'c-news__body'})

    if content is not None:
        for x in content.findChildren('p'):
            full_text += x.text
    else:
        content = soup.find(
            'div', attrs={'class': 'news-content content'})
        if content is not None:
            for x in content.findChildren('p'):
                full_text += x.text

    return full_text


def get_news_urls(url_base):
    page = requests.get(url_base)
    soup = BeautifulSoup(page.content, 'html.parser')

    news_feed = soup.select_one(
        '#conteudo > div.page > div:nth-of-type(6) > div > div > div.flex-cell > div > div > div > ol')

    url_list = []
    news_feed = news_feed.find_all('a', href=True)

    for n in news_feed:
        print(n['href'])
        url_list.append(n['href'])

    final_url_list = list(set(url_list))
    print(len(final_url_list))
    print(len(url_list))

    f_lst = list(filter(
        lambda x: 'https://www1.folha.uol.com.br/poder/eleicoes/2018' not in x, final_url_list))
    print(len(f_lst))

    return f_lst


def main():
    url_base = 'https://www1.folha.uol.com.br/poder/eleicoes/2018/#90'
    urls_list = get_news_urls(url_base)

    news_list = []

    for url in urls_list:
        new = get_full_news(url)
        news_list.append(new)

    path = '../datasets/folha_sp/all_news.csv'

    with open(path, 'a') as f:
        writer1 = csv.writer(f, delimiter='|')
        for n in news_list:
            writer1.writerow(
                [n])
        f.close()


if __name__ == '__main__':
    main()
