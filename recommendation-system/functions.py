import math
import random

import matplotlib.pyplot as plt
import numpy as np

ORIGINAL_DATA_PATH = 'recommendation-system/data/data.csv'
SAMPLE_DATA_PATH = 'recommendation-system/data/learning_sample.csv'
TEST_DATA_PATH = 'recommendation-system/data/test_sample.csv'

MARKED_AS_NULL = '99'


# loads and returns data from csv file
def load_data(path):
    preferences = {}
    counter = 0
    with open(path) as file:
        for line in file:
            preferences.setdefault(counter, {})
            rates = line.split(',')
            for i in range(len(rates)):
                if rates[i] != MARKED_AS_NULL:
                    preferences[counter][i] = float(rates[i])
            counter += 1
    return preferences


def load_original_data():
    return load_data(ORIGINAL_DATA_PATH)


def load_test_data():
    return load_data(TEST_DATA_PATH)


def load_sample_data():
    return load_data(SAMPLE_DATA_PATH)


def export_to_file(preferences, file_path):
    with open(file_path, 'w') as file:
        for i in range(len(preferences)):
            file.write(','.join([str(preferences[i][j]) if j in preferences[i] else MARKED_AS_NULL
                                 for j in range(100)]) + "\n")


def get_inverted_data(preferences):
    result = {}
    for i in preferences:
        for j in preferences[i]:
            if not j in result:
                result.setdefault(j, {})
            result[j][i] = preferences[i][j]
    return result


# moves a specified percent of the data to the test matrix and returns it
def generate_test_sample(preferences, percent):
    height = len(preferences)
    test_size = height * percent
    test = {}
    for i in range(test_size):
        print i
        user = random.choice(preferences.keys())
        if not user in test:
            test.setdefault(user, {})
        item = random.choice(preferences[user].keys())
        test[user][item] = preferences[user][item]
        preferences[user].pop(item, None)
    return test


# draws matrix
def visualize(matrix):
    height = len(matrix)
    width = 100
    aa = np.zeros((width, height))
    for y in matrix:
        print 'y'
        for x in matrix[y]:
            print str(x) + ' ' + str(y)
            aa[x, y] = 1
    plt.imshow(aa, aspect='auto')
    plt.show()


# calculating euclidean distance between two vectors
def get_euclidean_distance(preferences, vector1, vector2):
    sum_of_squares = sum([pow(preferences[vector1][i] - preferences[vector2][i], 2)
                          for i in preferences[vector1] if i in preferences[vector2]])
    return 1 / (1 + math.sqrt(sum_of_squares)) if sum_of_squares > 0 else 0


# calculating jaccard index for two vectors
def get_jaccard_index(preferences, vector1, vector2):
    set1 = set(preferences[vector1].keys())
    set2 = set(preferences[vector2].keys())
    return float(len(set1 & set2)) / float(len(set1 | set2))


# returns top k matches for every vector
def get_top_matches_for_all_lines(preferences, similarity_function, k=5):
    scores = {}
    for i in preferences:
        print i
        score = [(similarity_function(preferences, i, other), other)
                 for other in preferences if other != i]
        score.sort()
        scores[i] = score[len(score) - k:]
    return scores


# returns predicted rate for 'item' element
def calculate_predicted_rate(preferences, item, top):
    total = sum([sim * (preferences[other][item] if item in preferences[other] else 0)
                 for (sim, other) in top])
    sum_of_sims = sum([sim for (sim, other) in top])
    return total / sum_of_sims


# calculates predicted rates and returns root mean square error between them and real ones
def calculate_rmse(sample_data, test_data, scores):
    errors = []
    for i in sample_data:
        print i
        top = scores[i]
        errors.extend([pow(test_data[i][j] - calculate_predicted_rate(sample_data, j, top), 2)
                       for j in test_data[i]])
    return math.sqrt(sum(errors) / len(errors))


# returns a tuple of RMSEs using euclidean and jaccard methods
def get_rmse_for_euclidean_and_jaccard_methods(sample_data, test_data):
    euclidean_top_matches = get_top_matches_for_all_lines(sample_data, get_euclidean_distance)
    jaccard_top_matches = get_top_matches_for_all_lines(sample_data, get_jaccard_index)

    return (calculate_rmse(sample_data, test_data, euclidean_top_matches),
            calculate_rmse(sample_data, test_data, jaccard_top_matches))


def test():
    print 'Loading...'
    original_data = load_original_data()
    sample_data_user_based = load_sample_data()
    test_data_user_based = load_test_data()

    print 'Done.'

    visualize(original_data)

    print 'User-based method:'

    (euclidean_rmse, jaccard_rmse) = get_rmse_for_euclidean_and_jaccard_methods(
        sample_data_user_based,
        test_data_user_based)

    print 'RMSE using Euclidean method: ' + str(euclidean_rmse)

    print 'RMSE using Jaccard method: ' + str(jaccard_rmse)

    print 'Item-based method:'

    sample_data_item_based = get_inverted_data(sample_data_user_based)
    test_data_item_based = get_inverted_data(test_data_user_based)

    (euclidean_rmse, jaccard_rmse) = get_rmse_for_euclidean_and_jaccard_methods(
        sample_data_item_based,
        test_data_item_based)

    print 'RMSE using Euclidean method: ' + str(euclidean_rmse)

    print 'RMSE using Jaccard method: ' + str(jaccard_rmse)
