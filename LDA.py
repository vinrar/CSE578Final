import time

import gensim
import nltk
import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
from gensim import corpora, models
import numpy as np


# category_name = 'Horror'

def lemmatize_stemming(text):
    stemmer = SnowballStemmer('english')
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


replace_words = {'mysteri': 'mystery', 'fantasi': 'fantasy', 'hous': 'house', 'leav': 'leave', 'littl': 'little',
                 'narrat': 'narrate', 'vampir': 'vampire', 'zombi': 'zombie', 'stori': 'story', 'servic': 'service',
                 'minut': 'minute', 'people': 'people', 'manag': 'manage', 'histori': 'history', 'compani': 'company',
                 'busi': 'business', 'pictur': 'picture', 'favorit': 'favorite', 'condit': 'conditioning',
                 'beginn': 'beginner', 'probabl': 'probable', 'imagin': 'imagine', 'complet': 'complete',
                 'charact': 'character', 'charli' : 'charlie', 'episod': 'episode', 'histori': 'history', 'illust': 'illustration',
                 'movi': 'movie', 'volum': 'volume', 'descrip': 'description', 'fortun': 'fortune', 'industri': 'industry',
                 'languag': 'language', 'easi' : 'easy', 'piec': 'piece', 'websit': 'website', 'theori': 'theory',
                 'abus': 'abuse', 'domin': 'domination', 'histor': 'history', 'justic': 'justice', 'ladi': 'lady',
                 'marri': 'marry', 'marriag': 'marriage', 'memori': 'memory', 'nightmar': 'nightmare', 'pleasur': 'pleasure',
                 'rememb': 'remember', 'babi': 'baby', 'beauti': 'beauty', 'charact': 'character', 'copi': 'copy',
                 'favorit': 'favorite', 'funni': 'funny', 'illustr': 'illustration', 'juic': 'juice', 'seri': 'serious',
                 'amaz': 'amaze', 'bibl': 'bible', 'biblographi': 'biblography', 'chines': 'chinese', 'countri': 'country',
                 'dictionari': 'dictionary', 'individu': 'individual', 'inspir': 'inspire', 'liberti': 'liberty', 'polit': 'politics',
                 'presid': 'president', 'romanc': 'romance', 'societi': 'society', 'struggl': 'struggle', 'translat': 'translate',
                 'winchest': 'winchester', 'beauti': 'beauty', 'funni': 'funny', 'movi': 'movie', 'peopl': 'people', 'puzzl': 'puzzle',
                 'seri': 'series', 'exampl': 'example', 'hilari': 'hilarious', 'peopl': 'people', 'polit': 'polite', 'adventur': 'adventure',
                 'copi': 'copy', 'famili': 'family', 'polici': 'policy', 'physic': 'physics', 'practic': 'practice', 'scienc': 'science',
                 'spirut': 'spirutual', 'univers': 'univserse', 'beauti': 'beautiful', 'favorit': 'favorite', 'funni': 'funny',
                 'histor': 'history', 'ladi': 'lady', 'condit': 'condition', 'famili': 'family', 'guid': 'guide', 'illustr': 'illustration',
                 'speci': 'species', 'theori': 'theory', 'univers': 'universe', 'bodi': 'body', 'leagu': 'league', 'stori': 'story',
                 'adventur': 'adventure', 'countri': 'country', 'easi': 'easy', 'faimili': 'family', 'peopl': 'people'
                 }


def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result


genre_frequency_file = open('./Data/genre/genre_frequency.csv', "r")

for genre_frequency in genre_frequency_file:
    # reviews_json = open('Books.json', 'r')
    print(genre_frequency)
    values = genre_frequency.split(',')
    category_name = values[0]
    if '#' in category_name:
        continue

    data = pd.read_csv('./Data/mergedReview/' + category_name.replace(' ', '') + '_asin_review_merged.csv',
                       error_bad_lines=False)
    data.columns = ['name', 'headline_text']
    data_text = data[['headline_text']]
    data_text['index'] = data_text.index
    documents = data_text

    print(len(documents))
    print(documents[:5])

    np.random.seed(2018)
    nltk.download('wordnet')

    doc_sample = documents[documents['index'] == 2].values[0][0]
    print('original document: ')
    words = []
    for word in doc_sample.split(' '):
        words.append(word)
    print(words)
    print('\n\n tokenized and lemmatized document: ')
    print(preprocess(doc_sample))

    processed_docs = documents['headline_text'].map(preprocess)
    print(processed_docs[:10])

    dictionary = gensim.corpora.Dictionary(processed_docs)
    count = 0
    for k, v in dictionary.iteritems():
        print(k, v)
        count += 1
        if count > 10:
            break

    dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

    bow_corpus = [dictionary.doc2bow(doc, True) for doc in processed_docs]
    print(bow_corpus[0])

    bow_doc_0 = bow_corpus[0]
    for i in range(len(bow_doc_0)):
        print("Word {} (\"{}\") appears {} time.".format(bow_doc_0[i][0],
                                                         dictionary[bow_doc_0[i][0]], bow_doc_0[i][1]))

    tfidf = models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]
    from pprint import pprint

    # for doc in corpus_tfidf:
    #     pprint(doc)
    #     break

    start_time = time.time()
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)

    subGenre_percentage = {}
    for idx, topic in lda_model.print_topics(-1):
        print('Topic: {} \nWords: {}'.format(idx, topic))
        topic_percentages = topic.split('" + ')
        for topic_percentage in topic_percentages:
            values = topic_percentage.split('*"')
            sub_genre = values[1]
            value = float(values[0])
            if '"' in sub_genre:
                continue
            if sub_genre in subGenre_percentage:
                if value > subGenre_percentage[sub_genre]:
                    subGenre_percentage[sub_genre] = value
            else:
                subGenre_percentage[sub_genre] = value
            print(topic_percentage)

    sub_genre_score_file = open('./Data/subgenre_score/' + category_name.replace(" ", "") + "_subgenre_score.csv", "w+")

    for subGenre, value in sorted(subGenre_percentage.items(), key=lambda item: item[1], reverse=True):
        if subGenre in replace_words:
            sub_genre_score_file.write(replace_words[subGenre] + ',' + str(value) + '\n')
        else:
            sub_genre_score_file.write(subGenre + ',' + str(value) + '\n')

    sub_genre_score_file.close()

    end_time_1 = time.time()
    print("Time1: " + str(end_time_1 - start_time))

    print(len(bow_corpus))

    topic_asin_map = {}
    for subGenre in subGenre_percentage:
        topic_asin_map[subGenre] = {}

    for i in range(0, len(bow_corpus)):
        print(data['name'][i])
        for index, score in sorted(lda_model[bow_corpus[i]], key=lambda tup: -1 * tup[1]):
            topic = lda_model.print_topic(index, 10)
            topic_percentages = topic.split('" + ')
            for topic_percentage in topic_percentages:
                values = topic_percentage.split('*"')
                sub_genre = values[1]
                if '"' in sub_genre:
                    continue
                value = score * float(values[0]) * 100
                book_score_dict = {}
                asin = data['name'][i]
                topic_asin_map[sub_genre][asin] = value

            print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))

    for subGenre, value in sorted(subGenre_percentage.items(), key=lambda item: item[1], reverse=True):
        asin_percentage_map = topic_asin_map[subGenre]

        if subGenre in replace_words:
            sub_genre_book_score_file = open(
                './Data/subgenre_books/table_' + category_name.replace(" ", "") + "_" + replace_words[
                    subGenre] + "_subgenre_books_score.csv", "w+")
        else:
            sub_genre_book_score_file = open(
                './Data/subgenre_books/table_' + category_name.replace(" ",
                                                                       "") + "_" + subGenre + "_subgenre_books_score.csv",
                "w+")

        count = 0
        max_score = 0
        for book, percentage in sorted(asin_percentage_map.items(), key=lambda item: item[1], reverse=True):
            if percentage > max_score:
                max_score = percentage
            count += 1
            sub_genre_book_score_file.write(str(book) + "," + str(round((percentage * 100) / max_score)) + "\n")
            if count == 10:
                break

    print(topic_asin_map)

    end_time_2 = time.time()
    print("Time2: " + str(end_time_2 - end_time_1))
