import numpy as np


def linear_backward(d: np.ndarray, X: np.ndarray, W: np.ndarray, b: np.ndarray):
    dX = np.dot(d, W.T).reshape(X.shape)
    dW = np.dot(X.reshape(-1, W.shape[0]).T, d)
    db = d.sum(0)

    return dX, dW, db


def linear(X: np.ndarray, W: np.ndarray, b: np.ndarray):
    return np.dot(X, W) + b, (X, W, b)


def sigmoid(X: np.ndarray):
    return 1 / (1 + np.exp(-X))


def relu_backward(d: np.ndarray, X: np.ndarray):
    dx = d
    dx[X <= 0] = 0
    return dx


def relu(X: np.ndarray):
    return np.maximum(0, X)


class NNet:

    def __init__(self, hidden_dims: list = [500], num_cls: int = 2,
                 input_dim: int = 400, std: float = 1e-4):
        self.params = {}
        self.params['W1'] = std * np.random.randn(input_dim, hidden_dims[0])
        self.params['b1'] = np.zeros(hidden_dims[0])
        for i in range(1, len(hidden_dims) - 1):
            self.params['W%d' % (i + 1)] = std * np.random.randn(hidden_dims[i - 1], hidden_dims[i])
            self.params['b%d' % (i + 1)] = np.zeros(hidden_dims[i])
        self.params['W%d' % (len(hidden_dims))] = std * np.random.randn(hidden_dims[-1], num_cls)
        self.params['b%d' % (len(hidden_dims))] = np.zeros(num_cls)
        self.num_layers = len(hidden_dims) + 1

    def loss(self):
        pass

    def train(self, X: np.ndarray, y: np.ndarray,
              X_val: np.ndarray, y_val: np.ndarray,
              lr: float = 1e-3, num_epochs: int = 10, batch_size=200):
        pass

    def predict(self, X: np.ndarray):
        A = X.copy()
        for i in range(self.num_layers - 1):
            A = linear(A, self.params["W%d" % (i + 1)], self.params["b%d" % (i + 1)])
            A = relu(A)
        A = linear(A, self.params["W%d" % self.num_layers], self.params["b%d" % self.num_layers])
        return sigmoid(A)


if __name__ == '__main__':
    ...
