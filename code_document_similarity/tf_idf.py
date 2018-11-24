import nltk
from collections import OrderedDict

corpus = {
    'a': "Mr. Green killed Colonel Mustard in the study with the candlestick. Mr. Green is not a very nice fellow.",
    'b': "Professor Plum has a green plant in his study.",
    'c': "Miss Scarlett watered Professor Plum's green plant while he was away from his office last week."}

ordered_corpus = OrderedDict(sorted(corpus.items(), key=lambda t: t[0]))
print(ordered_corpus)
text_list = [y.lower().split() for x, y in ordered_corpus.iteritems()]
nltk_repr = nltk.TextCollection(text_list)
query1 = 'green'
idx = 0
for title, text in ordered_corpus.iteritems():
    score = 0
    score += nltk_repr.tf(query1, text_list[idx])
    idx += 1
    print('tf score for ', title, ' ', 'is', ' ', str(score))
idx = 0
for title, text in ordered_corpus.iteritems():
    score = 0
    score += nltk_repr.tf_idf(query1, text_list[idx])
    idx += 1
    print('tf_idf score for ', title, ' ', 'is', ' ', str(score))
print('idf of "', query1, '"  for corpus is ',
      nltk_repr.idf(query1, text_list))


def tf_the_hard_way():
    pass


def idf_the_hard_way():
    pass


def tf_idf_the_hard_way():
    pass
