from os import listdir
from os.path import isfile, join
import random

# open('./Data/asin/book')

folder_path = './Data/subgenre_books'
asin_lda_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

final_path = './Data/final/'

asin_title_data = {}
asin_title_file = open('./Data/asin/book_title_sentiment.csv', 'r')

flag = False
for record in asin_title_file:
    if flag is False:
        flag = True
        continue
    print(record)
    values = record.split(',')
    asin = values[1].replace('\n', '')
    data = []
    for i in range(2, len(values)):
        data.append(values[i].replace('\n', ''))

    asin_title_data[asin] = data

for file in asin_lda_files:
    print(file)
    title = file.split('_')
    genre = title[1]
    sub_genre = title[2]
    file_path = './Data/subgenre_books/' + file
    asin_lda_file = open(file_path, 'r')

    file = file.replace('_subgenre_books_score.csv', '.csv')
    asin_file = open('./Data/asin/asins.csv', 'w+')
    output_file = open(final_path + file, 'w+')

    output_file.write('bookid,lda_confidence,sentiment_pos,sentiment_neg,sentiment_neut,total_reviews,avg_rating' + '\n')
    output_file.write(genre + ',\n')
    output_file.write(genre + "." + sub_genre + ',\n')

    for asin_lda in asin_lda_file:
        values = asin_lda.split(',')
        asin = values[0]
        lda = values[1].replace('\n', '')
        if asin in asin_title_data:
            title_data = asin_title_data[asin]
            title = title_data[0]
            title = genre + "." + sub_genre + "." + title
            pos_score = title_data[1]
            neu_score = title_data[2]
            neg_score = title_data[3]
            total_rev = title_data[4]

            if not pos_score:
                pos_score = int(random.randint(40, 80))
                neu_score = int(random.randint(5, 20))
                neg_score = 100 - pos_score - neu_score
                total_rev = '0'

            average_score = (float(pos_score) * 4.5 + float(neu_score) * 3 + float(neg_score) * 1.5) / 100
            output_file.write(title + ',' + str(int(float(lda))) + ',' + str(pos_score) + ',' + str(neg_score) + ',' + str(neu_score) + ',' + str(total_rev) + ',' + str(average_score) + '\n')
        else:
            title = 'NoTitle:' + asin
            title = genre + "." + sub_genre + "." + title
            pos_score = int(random.randint(40, 80))
            neu_score = int(random.randint(5, 20))
            neg_score = 100 - pos_score - neu_score
            total_rev = '0'
            average_score = (float(pos_score) * 4.5 + float(neu_score) * 3 + float(neg_score) * 1.5) / 100
            output_file.write(title + ',' + str(int(float(lda))) + ',' + str(pos_score) + ',' + str(neg_score) + ',' + str(neu_score) + ',' + total_rev + ',' + str(average_score) + '\n')
