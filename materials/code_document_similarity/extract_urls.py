from bs4 import BeautifulSoup
import urllib2
with open('source.html','r') as f:
    soup = BeautifulSoup(f.read())
    list_of_urls = soup.find_all('a')
    for tags in list_of_urls:
         url = tags.get('href')
         if 'ycombinator' not in url:
            if 'hckrnews' not in url:
                print url