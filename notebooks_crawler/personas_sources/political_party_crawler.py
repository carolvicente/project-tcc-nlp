import requests
import csv
from bs4 import BeautifulSoup

URL = 'http://www.tse.jus.br/partidos/partidos-politicos'


def get_party_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    item_list = soup.findChildren('section')[1].findChild(
        'div').findChild('div').findChildren('p')
    initials = ''
    party_url = ''

    for item in item_list:
        url_list = item.find_all('a', href=True) if party_url == '' else False
        if url_list:
            party_url = url_list[0]['href']

    return str(party_url)


def main():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.findChild('table').findChild('tbody')
    rows = table.findChildren('tr')
    status = 0
    count = 0
    initials = ''
    party_name = ''
    lider_name = ''
    tse_url = ''
    party_url = ''

    with open('../../data/external/political_party.csv', 'w') as csvfile:
        fw = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fw.writerow(['Party_name', 'Lider_name',
                     'Popular_lider_name', 'Tse_url', 'Party_url'])
        for row in rows:

            info = row.findChildren('td')
            print('Crawling ...', status)
            print('----------------------')
            if len(info) >= 6:
                url = info[1].find_all('a', href=True)[0]
                tse_url = url['href']
                party_url = get_party_url(tse_url).replace('|', '')
                idx_party = len(info[2].contents) - 1
                party_name = str(info[2].contents[idx_party])
                lider_name = str(info[4].contents[0])
                lider_name = lider_name.replace(
                    '<p>', '').replace('</p>', '').replace('<span>', '').replace('</span>', '').replace(
                        ', no exercício da presidência|', '').replace('|', '').replace(
                            '<span id="form:grupoPrincipal">', '').replace(', no exercício da presidência', '')
                popular_lider_name = ''
                fw.writerow([party_name, lider_name,
                             popular_lider_name, tse_url, party_url])

            status += 1


if __name__ == '__main__':
    main()
