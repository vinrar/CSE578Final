import json

asin_file = open('./Data/asin/asins.csv', 'r')
asins = set()

for asin in asin_file:
    asins.add(asin.replace('\n', ''))

ratings_file = open('./meta.json', 'r')
meta_json = open("meta.json", "r")
asin_title = open('./Data/asin/asin_title.csv', 'w+')
count = 0

for each_json in meta_json:
    json1_data = json.loads(each_json)
    if 'title' in json1_data and 'asin' in json1_data:
        asin = json1_data['asin']
        title = json1_data['title']
        if asin in asins:
            print(asin + ":" + title)
            asin_title.write(asin + "," + title.replace(',', '') + '\n')
            count += 1

print(count)
print(len(asins))
