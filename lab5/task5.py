import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import matplotlib.pyplot as plt

from task1 import get_data, split_data


EMBEDDINGS_TEST_SET_FILE = "jokes/embeddings_test_set.npy"
TEST_JOKES = [
    "Why Java programmers wear glasses? Because they can't c#",
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "This couple had an excellent relationship going until one day he came home from work to find his girlfriend packing. \
        He asked her why she was leaving him and she told him that she had heard awful things about him. \
            What could they possibly have said to make you move out? They told me that you were a pedophile. \
                He replied, That's an awfully big word for a ten year old.",
    "I went to the doctors recently He said: Don’t eat anything fatty I said: What, like bacon and burgers? \
        He said, No. fatty don’t eat anything",
    "Why do you never see hippos hiding in trees Because they're very good at it.",
    "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE \
        EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE \
              EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
]


CONFIG = {
    "constant": {
        "max_iter": 200,
        "learning_rate": "constant",
        "alpha": 0.001,
        "hidden_layer_sizes": (10,)
    },
    "invscaling": {
        "max_iter": 600,
        "learning_rate": "invscaling",
        "alpha": 1.0,
        "hidden_layer_sizes": (50,)
    },
    "adaptive": {
        "max_iter": 200,
        "learning_rate": "adaptive",
        "alpha": 10.0,
        "hidden_layer_sizes": (50,)
    }
}

def extract_test_features(jokes):
    if os.path.isfile(EMBEDDINGS_TEST_SET_FILE):
        existing = np.load(EMBEDDINGS_TEST_SET_FILE)
        if existing.shape[0] == len(jokes):
            return existing
        else:
            os.remove(EMBEDDINGS_TEST_SET_FILE)

    # extract features from jokes using BERT
    model = SentenceTransformer('bert-base-cased')
    embeddings = model.encode(jokes)
    # serialize embeddings
    np.save(EMBEDDINGS_TEST_SET_FILE, embeddings)
    return embeddings


def train_predict(data, configs):
    test_jokes = extract_test_features(TEST_JOKES)
    print(f"Test jokes: {test_jokes.shape}")

    results = []
    # iterate over different configurations
    # collect results (predicted ratings) for each configuration
    # plot results as scatter plot
    for config_name, config in configs.items():
        X_train, X_test, y_train, y_test = split_data(data)
        model = MLPRegressor(solver='sgd', **config)
        model.fit(X_train, y_train)

        y_pred = model.predict(test_jokes)
        results.append(y_pred)

        print(f"Config: {config_name}")
        print(f"Mean squared error: {mean_squared_error(y_test, model.predict(X_test))}")
        print(f"Mean absolute error: {mean_absolute_error(y_test, model.predict(X_test))}")
        print(f"R2 score: {r2_score(y_test, model.predict(X_test))}")
        print()

    # plot results
    plt.figure(figsize=(7, 7))
    plt.scatter(range(len(TEST_JOKES)), results[0], label="constant")
    plt.scatter(range(len(TEST_JOKES)), results[1], label="invscaling")
    plt.scatter(range(len(TEST_JOKES)), results[2], label="adaptive")
    # plot index of joke on x-axis
    plt.xticks(range(len(TEST_JOKES)), range(1, len(TEST_JOKES) + 1))
    # plot error on y axis

    plt.title("Prediction results of custom jokes")
    plt.ylabel("Predicted rating")
    plt.xlabel("Joke")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    data = get_data()
    train_predict(data, CONFIG)
