import csv

DATA_NEGATIVE_CSV = 'sentiment-analysis/data/negative.csv'

DATA_POSITIVE_CSV = 'sentiment-analysis/data/positive.csv'


def load_data(file_path):
    with open(file_path) as file:
        return list(csv.reader(file, delimiter=';', quotechar='\"'))


def load_positive_data():
    return load_data(DATA_POSITIVE_CSV)


def load_negative_data():
    return load_data(DATA_NEGATIVE_CSV)


pos = load_positive_data()
neg = load_negative_data()
