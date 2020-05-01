from os import listdir
from os.path import isfile, join
import random


folder_path = './Data/subgenre_score'
output_folder_path = './Data/final_subgenre_score/'
subgenre_score_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]


for subgenre_score_file in subgenre_score_files:
    values = subgenre_score_file.split('_')
    genre = values[0]
    output_file_name = "bubble_" + genre + ".csv"
    output_file = open(output_folder_path + output_file_name, 'w')

    input_file = open(folder_path + "/" + subgenre_score_file, 'r')

    output_file.write("id,value\n")
    for each_line in input_file:
        output_file.write("1." + each_line)

    output_file.close()
    input_file.close()