import nltk
from nltk.stem.porter import *
stemmer = PorterStemmer()
with open('alice', 'r') as f:
    read_text = f.read()

tokens = read_text.split()

text = nltk.Text(tokens)

"""for t in tokens:
	print t,stemmer.stem(t)"""

# Word frequency count
freq = nltk.FreqDist(tokens)
for word, count in freq.iteritems():
    print word, count
