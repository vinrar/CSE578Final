asin_file = open('./Data/asin/asins.csv', 'r')
asins = set()

for asin in asin_file:
    asins.add(asin.replace('\n', ''))

ratings_file = open('./ratings.csv', 'r')

count = 0
found = set()
for record in ratings_file:
    values = record.split(',')
    asin = values[1].replace('\n', '')
    # print(values)
    # print(asin)
    if asin in asins:
        if asin not in found:
            found.add(asin)
            count += 1
        print(asin)


print(count)
print(len(asins))
