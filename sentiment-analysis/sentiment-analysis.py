import csv
from random import shuffle

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer

DATA_NEGATIVE_CSV = 'sentiment-analysis/data/negative.csv'

DATA_POSITIVE_CSV = 'sentiment-analysis/data/positive.csv'


def load_data(file_path):
    with open(file_path) as file:
        return list(csv.reader(file, delimiter=';', quotechar='\"'))


def load_positive_data():
    return load_data(DATA_POSITIVE_CSV)


def load_negative_data():
    return load_data(DATA_NEGATIVE_CSV)


def get_text_list_and_tonal_list(data):
    return [i[3] for i in data], [i[4] for i in data]


def get_all_data_shuffled():
    data = load_positive_data()
    data.extend(load_negative_data())
    shuffle(data)
    return data


def get_train_and_test_data(data, test_size=0.2):
    train = data[:int(len(data) * test_size)]
    test = data[int(len(data) * test_size):]
    return train, test


def test(nb, max_features=3000):
    data = get_all_data_shuffled()
    train, test = get_train_and_test_data(data)
    train_text, train_tonal = get_text_list_and_tonal_list(train)
    test_text, test_tonal = get_text_list_and_tonal_list(test)

    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=max_features)

    train_vectors = vectorizer.fit_transform(train_text)
    test_vectors = vectorizer.fit_transform(test_text)
    fitted = nb.fit(train_vectors.toarray(), train_tonal)
    result = fitted.predict(test_vectors.toarray())
    return round(metrics.accuracy_score(test_tonal, result), 3)
