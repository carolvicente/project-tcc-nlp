import urllib2
import urllib
import json 

token = ''
diffbot_prefix = 'http://api.diffbot.com/v2/article'
delimiter = '&'
result_list = []
with open('top_urls.txt','r') as f:
    cnt = 0
    for url in f:
        diffbot_url = ''.join([diffbot_prefix, "?",'token=',token,delimiter,'url=',url])
        print diffbot_url
        try:
            req = urllib2.Request(diffbot_url)
            val = urllib2.urlopen(diffbot_url,timeout=60)
            response =  val.read()
            result_list.append(response)
        except IOError as e:
            print e
            continue

with open('hn.json', 'a') as hn:
    hn.write(json.dumps(result_list, indent=1))
