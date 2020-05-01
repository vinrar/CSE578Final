from os import listdir
from os.path import isfile, join


asin_file = open('./Data/asin/asins.csv', 'r')
asins = set()

for asin in asin_file:
    # print(asin)
    asins.add(asin.replace('\n', ''))

# print(asins)
book_sentiment_freq = open('./Data/asin/book_sentimentFrequency.csv', 'r')

count = 0
for record in book_sentiment_freq:
    if count is 0:
        count += 1
        continue

    values = record.split(',')
    asin = values[1]
    if asin in asins:
        print(asin)
