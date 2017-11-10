import csv
import math
import random

import matplotlib.pyplot as plt
import numpy as np


def load_data(path):
    matrix = []
    with open(path) as file:
        for line in file:
            matrix.append([float(rate) for rate in line.split(',')])
    return matrix


def load_original_data():
    return load_data('recommendation-system/data/data.csv')


def load_test_data():
    return load_data('recommendation-system/data/test_sample.csv')


def load_sample_data():
    return load_data('recommendation-system/data/learning_sample.csv')


def export_to_file(matrix, file_path='/tmp/data.csv'):
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


def visualize(matrix):
    height = matrix.__len__()
    width = matrix[0].__len__()
    aa = np.zeros((width, height))
    for i in range(height):
        for j in range(width):
            if matrix[i][j] != 99:
                aa[j, i] = 1
    plt.imshow(aa, aspect='auto')
    plt.show()


def euclidean_distance_by_person(preferences, person1, person2):
    sum_of_squares = sum([pow(preferences[person1][i] - preferences[person2][i], 2)
                          for i in range(preferences[person1].__len__())
                          if preferences[person1][i] != 99 and preferences[person2][i] != 99])

    return 1 / (1 + math.sqrt(sum_of_squares)) if sum_of_squares > 0 else 0


def jaccard_index_by_person(preferences, person1, person2):
    set1 = set(preferences[person1])
    set2 = set(preferences[person2])
    return float(len(set1.intersection(set2))) / float(len(set1.union(set2)))
