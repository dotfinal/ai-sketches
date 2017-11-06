import csv
import random

def load_data(path = 'recommendation-system/data/data.csv'):
    matrix = []
    with open(path) as file:
        for line in file:
            matrix.append([float(rate) for rate in line.split(',')])
    return matrix

def export_to_file(matrix, file_path = '/tmp/data.csv'):
    with open(file_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(matrix)

# moves a specified percent of the data to the test matrix and returns it
def generate_test_sample(matrix, percent):
    height = matrix.__len__()
    width = matrix[0].__len__()
    counter = width * height * percent / 100
    test = [[99] * width for i in range(height)]
    print counter
    while counter > 0:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if matrix[y][x] != 99:
            test[y][x] = matrix[y][x]
            matrix[y][x] = 99
            counter -= 1
    return test
