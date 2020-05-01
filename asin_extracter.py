from os import listdir
from os.path import isfile, join

mypath = './Data/subgenre_books'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

asin_file = open('./Data/asin/asins.csv', 'w+')

for file in onlyfiles:
    print(file)
    file_path = './Data/subgenre_books/' + file
    csv_file = open(file_path, 'r')
    for each_line in csv_file:
        print(each_line)
        values = each_line.split(',')
        asin = values[0]
        asin_file.write(asin + '\n')