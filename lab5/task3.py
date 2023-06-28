from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns
import pandas as pd
from task1 import get_data, split_data


def evaluate_model(X_train, X_test, y_train, y_test, learning_rates=["constant", "invscaling", "adaptive"],
                   max_iter=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]):
    data: dict[str, list] = {}
    # data holds the mse, rmse, mae and r2 for each learning rate and max iter
    for learning_rate in learning_rates:
        mse_values = []
        rmse_values = []
        mae_values = []
        r2_values = []
        for iter in max_iter:
            model = MLPRegressor(solver='sgd', alpha=0.0, learning_rate=learning_rate, max_iter=iter)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            rmse = mean_squared_error(y_test, y_pred, squared=False)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            print("learning rate: ", learning_rate, "max iter: ", iter, "mse: ", mse)
            mse_values.append(mse)
            rmse_values.append(rmse)
            mae_values.append(mae)
            r2_values.append(r2)
        data[learning_rate] = {"mse": mse_values, "rmse": rmse_values, "mae": mae_values, "r2": r2_values}
    return data


def plot_metrics(metrics: dict[str, list], max_iter=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]):
    # for each learning rate, plot the mse, rmse, mae and r2 as a function of max iter
    # each learning rate would have a different color

    # plot mse, x axis: max iter, y axis: mse
    for i, learning_rate in enumerate(metrics.keys()):
        plt.plot(max_iter, metrics[learning_rate]["mse"], label=learning_rate)
    plt.title('MSE over max iter per learning rate')
    plt.xlabel('Max iter')
    plt.ylabel('MSE')
    plt.legend()
    plt.show()
    plt.savefig('mse_over_max_iter_per_learning_rate.png')

    # plot rmse, x axis: max iter, y axis: rmse
    for i, learning_rate in enumerate(metrics.keys()):
        plt.plot(max_iter, metrics[learning_rate]["rmse"], label=learning_rate)
    plt.title('RMSE over max iter per learning rate')
    plt.xlabel('Max iter')
    plt.ylabel('RMSE')
    plt.legend()
    plt.show()
    plt.savefig('rmse_over_max_iter_per_learning_rate.png')

    # plot mae, x axis: max iter, y axis: mae
    for i, learning_rate in enumerate(metrics.keys()):
        plt.plot(max_iter, metrics[learning_rate]["mae"], label=learning_rate)
    plt.title('MAE over max iter per learning rate')
    plt.xlabel('Max iter')
    plt.ylabel('MAE')
    plt.legend()
    plt.show()
    plt.savefig('mae_over_max_iter_per_learning_rate.png')

    # plot r2, x axis: max iter, y axis: r2
    for i, learning_rate in enumerate(metrics.keys()):
        plt.plot(max_iter, metrics[learning_rate]["r2"], label=learning_rate)
    plt.title('R2 over max iter per learning rate')
    plt.xlabel('Max iter')
    plt.ylabel('R2')
    plt.legend()
    plt.show()
    plt.savefig('r2_over_max_iter_per_learning_rate.png')


def accuracy_per_learning_rate(data, learning_rates=["constant", "invscaling", "adaptive"],
                               max_iter=[200, 400, 600, 800, 1000, 1500, 2000, 5000, 10000]):
    # train model for different learning rates and epochs
    # plot accuracy for each learning rate as a function of epochs
    # each learning rate would have a different color
    X_train, X_test, y_train, y_test = split_data(data)

    # train model
    for learning_rate in learning_rates:
        mse_values = []
        for iter in max_iter:
            model = MLPRegressor(solver='sgd', alpha=0.0, learning_rate=learning_rate, max_iter=iter)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            print("learning rate: ", learning_rate, "max iter: ", iter, "mse: ", mse)
            mse_values.append(mse)
        plt.plot(max_iter, mse_values, label=learning_rate)

    plt.title("mse per learning rate")
    plt.xlabel("max iter")
    plt.ylabel("mse")
    plt.legend()
    plt.show()


def accuracy_per_learning_rate_alpha(data, learning_rates=["constant", "invscaling", "adaptive"],
                                     max_iter=[100, 200, 500, 1000, 2000, 5000, 10000],
                                     alphas=[0.0001, 0.001, 0.01, 0.1, 1, 10]):
    X_train, X_test, y_train, y_test = split_data(data)

    for learning_rate in learning_rates:
        # Initialize matrix to store MSE values
        mse_values = np.zeros((len(alphas), len(max_iter)))

        for i, alpha in enumerate(alphas):
            for j, iter in enumerate(max_iter):
                model = MLPRegressor(solver='sgd', alpha=alpha, learning_rate=learning_rate, max_iter=iter)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                mse_values[i, j] = mse

        # Convert MSE matrix to DataFrame for easier plotting
        mse_df = pd.DataFrame(mse_values, index=alphas, columns=max_iter)

        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(mse_df, annot=True, fmt=".2f", cmap="YlGnBu")
        plt.title(f"MSE for learning rate: {learning_rate}")
        plt.xlabel("max iter")
        plt.ylabel("alpha")
        plt.show()


if __name__ == '__main__':
    max_iter = [200, 400, 600, 800, 1000, 1500, 2000, 5000, 10000]

    data = get_data()
    X_train, X_test, y_train, y_test = split_data(data)
    metrics = evaluate_model(X_train, X_test, y_train, y_test, max_iter=max_iter)
    plot_metrics(metrics, max_iter=max_iter)
    accuracy_per_learning_rate(data, max_iter=max_iter)

    # data = get_data()
    accuracy_per_learning_rate_alpha(data, max_iter=max_iter)
