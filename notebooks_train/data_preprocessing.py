import nltk
from collections import OrderedDict


def load_data():
    corpus = {
        'a': "Mesmo quando quero falar sobre mim, não acho as palavras certas que \
                me classifiquem, sou um pouco de tudo o que há, do que eu gostaria \
                de ser, sou uma outra pessoa, alguem que não se existe, mas que parece \
                com um monte de gente, que como eu, não se encaixa em nada.",
        'b': "Um ato aleatório de bondade, por menor que seja, pode ter um tremendo \
            impacto na vida de outra pessoa.",
        'c': "O Caos é impaciente. É aleatório. E, acima de tudo, egoísta. Ele destrói \
                simplesmente em função da mudança, alimentando-se de si mesmo numa fome \
                 constante. Mas o Caos também pode ser atraente"}
    return corpus


def remove_stop_words(text_list):
    stopwords = nltk.corpus.stopwords.words('portuguese')
    filtered_text_list = []
    for l in text_list:
        filtered_sentence = [item for item in l if not item in stopwords]
        filtered_text_list.append(filtered_sentence)

    return filtered_text_list


def stemmering(text_list):
    stemmer = nltk.stem.RSLPStemmer()
    stemmered_text_list = []

    for l in text_list:
        stemmered_sentence = [stemmer.stem(item) for item in l]
        stemmered_text_list.append(stemmered_sentence)

    return stemmered_text_list


def main():
    corpus = load_data()
    ordered_corpus = OrderedDict(sorted(corpus.items(), key=lambda t: t[0]))
    text_list = [y.lower().split() for x, y in ordered_corpus.items()]

    new_text_list = remove_stop_words(text_list)
    print(text_list)
    print('############')
    print(new_text_list)
    stemmered_text_list = stemmering(new_text_list)
    print(stemmered_text_list)


if __name__ == "__main__":
    main()
