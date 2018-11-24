import json
import sys
import codecs
sys.stdout=codecs.getwriter('utf-8')(sys.stdout)


data = json.loads(open("hn.json").read())
for i in data:
    op=  json.loads(i)
    print op.get('title')

