import json

meta_json = open("category_ratingFrequency.json", "r")

categories = {}

count = 0
category_asins = open("category_frequency.csv", "w+")

genre_count_map = {}
for each_json in meta_json:
    each_json = each_json.replace('{', '')
    each_json = each_json.replace('}', '')
    values = each_json.split(', ')
    for value in values:
        finals = value.split(': ')
        if len(finals) == 2:
            name = finals[0].replace('"', '')
            value = finals[1]
            try:
                genre_count_map[name] = int(value)
            except ValueError:
                print(values)

genre_frequency_file = open('./Data/genre/genre_frequency.csv', "w+")
temp = 0
for book, count in sorted(genre_count_map.items(), key=lambda item: item[1], reverse=True):
    temp += 1
    print(book, count)
    genre_frequency_file.write(book + "," + str(count) + "\n")
    if temp == 60:
        break
