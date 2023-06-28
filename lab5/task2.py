from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

from task1 import get_data, split_data


def train_model(X_train, X_val, y_train, y_val):
    model = MLPRegressor(solver='sgd', alpha=0.0, learning_rate='constant')

    # train model
    model.fit(X_train, y_train)
    return model

    # # predict
    # train_predictions = model.predict(X_train)
    # val_predictions = model.predict(X_val)
    #
    # # calculate cost
    # train_cost = mean_squared_error(y_train, train_predictions)
    # val_cost = mean_squared_error(y_val, val_predictions)
    #
    # print(f'Train cost: {train_cost}, Validation cost: {val_cost}')


def cost_over_epochs_per_train_size(data, testing_set_sizes=[0.1, 0.2, 0.3, 0.4, 0.5]):
    # train model for different training set sizes
    # plot cost over epochs for each training set size
    # each would have a different color

    # train model
    for test_size in testing_set_sizes:
        X_train, X_val, y_train, y_val = split_data(data, test_size=test_size)
        model = train_model(X_train, X_val, y_train, y_val)
        # predict
        train_predictions = model.predict(X_train)
        val_predictions = model.predict(X_val)

        # calculate cost
        train_cost = mean_squared_error(y_train, train_predictions)
        val_cost = mean_squared_error(y_val, val_predictions)

        print(f'Train cost: {train_cost}, Validation cost: {val_cost}')

        plt.plot(model.loss_curve_, label=f'{(1 - test_size) * 100}% training set size')

    plt.title('Cost over epochs per training set size')
    plt.xlabel('Epochs')
    plt.ylabel('Cost')
    plt.legend()
    plt.show()
    plt.savefig('cost_over_epochs_per_train_size.png')






if __name__ == '__main__':
    data = get_data()
    cost_over_epochs_per_train_size(data)
    # X_train, X_val, y_train, y_val = split_data(data)
    # train_model(X_train, X_val, y_train, y_val)
