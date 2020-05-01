import json

categories = set()


genre_frequency_file = open('./Data/genre/genre_frequency.csv', "r")

for genre_frequency in genre_frequency_file:
    print(genre_frequency)
    values = genre_frequency.split(',')
    category_name = values[0]
    if '#' in category_name:
        continue
    file_name = './Data/books/' + category_name.replace(" ", "") + "_books.csv"
    category_asins = open(file_name, "w+")
    meta_json = open("meta.json", "r")
    count = 0
    for each_json in meta_json:
        # print(count)
        json1_data = json.loads(each_json)

        try:
            if 'category' in json1_data:
                book_categories = json1_data['category']
                if category_name in book_categories:
                    if 'asin' in json1_data:
                        print(count)
                        count += 1
                        category_asins.write(json1_data['asin'] + '\n')
                        if count > 150:
                            break
                    # print(json1_data['asin'])
        except KeyError:
            print('no category')
        except ValueError:
            print('file name and path: ' + file_name)

    print(categories)
    category_asins.close()
    meta_json.close()
