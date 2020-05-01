import json

genre_frequency_file = open('./Data/genre/genre_frequency.csv', "r")

for genre_frequency in genre_frequency_file:
    reviews_json = open('Books.json', 'r')
    count = 0
    print(genre_frequency)
    values = genre_frequency.split(',')
    category_name = values[0]
    if '#' in category_name:
        continue

    # category_asins = open('./Data/books/' + category_name.replace(" ", "") + "_books.csv", "r")
    #
    # asin_review = open('./Data/review/' + category_name.replace(" ", "") + "_asin_review.csv", "w+")
    # category_books_set = set()
    #
    # for category_asin in category_asins:
    #     category_books_set.add(category_asin.replace('\n',''))
    #
    # for each_review_json in reviews_json:
    #     each_review_data = json.loads(each_review_json)
    #     if 'asin' in each_review_data and 'reviewText' in each_review_data:
    #         asin = each_review_data['asin']
    #         review_text = each_review_data['reviewText']
    #         if asin in category_books_set:
    #             count += 1
    #             asin_review.write(asin + "," + review_text.replace(',',' ').replace('\n', ' ').replace('\r', '') + "\n") # replace all commas in asin_review with spaces
    #             if count > 7000:
    #                 break
    #             print(each_review_data)
    #
    # print("reviews extracted!")
    # asin_review.close()
    # reviews_json.close()
    # category_asins.close()
    # print("reviews merging!")

    asin_review = open('./Data/review/' + category_name.replace(" ", "") + "_asin_review.csv", "r")
    merged_asin_review = open('./Data/mergedReview/' + category_name.replace(" ", "") + "_asin_review_merged.csv", "w+")

    prev_asin = ''
    merged_review = ''
    first_time = True
    for each_asin_review in asin_review:
        values = each_asin_review.split(',')
        if values[0] in prev_asin:
            merged_review = merged_review + " " + values[1].replace('\n', '')
            print(merged_review)
        else:
            if first_time:
                first_time = False
            else:
                merged_asin_review.write(prev_asin + "," + merged_review + '\n')
            prev_asin = values[0]
            merged_review = values[1].replace('\n', '')

    merged_asin_review.close()