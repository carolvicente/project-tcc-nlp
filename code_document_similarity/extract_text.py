import urllib2
import os
import re
from nltk import clean_html
with open('top_urls.txt','r') as f:
    cnt = 0
    for url in f:
        #req = urllib2.Request(url)
        try:
            print url
            url = url.strip('\n\t')
            val = urllib2.urlopen(url,timeout=10)
            res = val.read()
            clean_text = clean_html(res)
            cleaner_text =  ' '.join(clean_text.split())
            file_name = 'file'+str(cnt)+'.txt'
            wf = open(file_name,'w+')
            wf.write(url)
            wf.write('\n')
            wf.write(cleaner_text)
            wf.close()
            cnt += 1
            break
        except IOError as e:
            print e
            continue