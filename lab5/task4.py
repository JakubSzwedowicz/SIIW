from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns
import pandas as pd
from task1 import get_data, split_data


def accuracy_per_neuron_number(data, learning_rates=["constant", "invscaling", "adaptive"],
                               max_iter=[100, 200, 500, 1000, 2000, 5000, 10000],
                               neuron_numbers=[10, 50, 100, 200, 500]):
    X_train, X_test, y_train, y_test = split_data(data)

    for learning_rate in learning_rates:
        # Initialize matrix to store MSE values
        mse_values = np.zeros((len(neuron_numbers), len(max_iter)))

        for i, neuron_number in enumerate(neuron_numbers):
            for j, iter in enumerate(max_iter):
                model = MLPRegressor(solver='sgd', hidden_layer_sizes=(neuron_number,), learning_rate=learning_rate,
                                     max_iter=iter)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                mse_values[i, j] = mse

        # Convert MSE matrix to DataFrame for easier plotting
        mse_df = pd.DataFrame(mse_values, index=neuron_numbers, columns=max_iter)

        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(mse_df, annot=True, fmt=".2f", cmap="YlGnBu")
        plt.title(f"MSE for learning rate: {learning_rate}")
        plt.xlabel("max iter")
        plt.ylabel("Number of Neurons")
        plt.show()


def accuracy_per_neuron_number_const(data, learning_rates=["constant", "invscaling", "adaptive"],
                                     max_iter=1000, alpha=0.01,
                                     neuron_numbers=[x for x in range(100, 2000, 50)]):
    X_train, X_test, y_train, y_test = split_data(data)
    # same as above, but use normal plot and not heatmap
    # also we are iterating over neuron numbers and not max iter/alpha
    for learning_rate in learning_rates:
        mse_values = []
        for neuron_number in neuron_numbers:
            model = MLPRegressor(solver='sgd', hidden_layer_sizes=(neuron_number,), learning_rate=learning_rate,
                                 max_iter=max_iter, alpha=alpha)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            mse_values.append(mse)
        plt.plot(neuron_numbers, mse_values, label=learning_rate)
    plt.legend()
    plt.title(f"MSE for different learning rates")
    plt.xlabel("Number of Neurons")
    plt.ylabel("MSE")
    plt.show()


if __name__ == '__main__':
    data = get_data()
    #accuracy_per_neuron_number(data)
    accuracy_per_neuron_number_const(data)
