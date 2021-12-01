import numpy as np
from typing import Tuple
from layers import (linear, linear_backward, relu, relu_backward,
                    mse_loss, sigmoid, softmax_loss,
                    softmax)
from optimizers import Optimizer


class NNet:

    def __init__(self, hidden_dims: list = [500], num_cls: int = 2,
                 input_dim: int = 400, std: float = 1e-4, loss: str = 'mse'):
        self.params = {}
        self.params['W1'] = std * np.random.randn(input_dim, hidden_dims[0])
        self.params['b1'] = np.zeros(hidden_dims[0])
        for i in range(1, len(hidden_dims) - 1):
            self.params['W%d' % (i + 1)] = std * np.random.randn(hidden_dims[i - 1], hidden_dims[i])
            self.params['b%d' % (i + 1)] = np.zeros(hidden_dims[i])
        self.params['W%d' % (len(hidden_dims))] = std * np.random.randn(hidden_dims[-1], num_cls)
        self.params['b%d' % (len(hidden_dims))] = np.zeros(num_cls)
        self.num_layers = len(hidden_dims) + 1
        if loss == 'mse':
            self.output_activation = sigmoid
            self.criterion = mse_loss
        else:
            self.output_activation = softmax
            self.criterion = softmax_loss

    def train(self, X: np.ndarray, y: np.ndarray,
              X_val: np.ndarray, y_val: np.ndarray,
              optimizer: Optimizer = Optimizer(),
              lr: float = 1e-3, num_epochs: int = 10, batch_size=64):
        pass

    def forward(self, X: np.ndarray) -> Tuple[list, dict]:
        hidden_layers_inputs, caches = [X], {}

        for i in range(self.num_layers - 1):
            h, cache = linear(hidden_layers_inputs[i], self.params["W%d" % (i + 1)], self.params["b%d" % (i + 1)])
            caches['linear%d' % (i + 1)] = cache
            h, cache = relu(hidden_layers_inputs[i])
            caches['relu%d' % (i + 1)] = cache
            hidden_layers_inputs.append(h)

        h, cache = linear(hidden_layers_inputs[-1], self.params['W%d' % self.num_layers],
                          self.params['b%d' % self.num_layers])

        hidden_layers_inputs.append(h)
        caches["linear%d" % self.num_layers] = cache

        return hidden_layers_inputs, caches

    def backward(self, X: np.ndarray, y: np.ndarray, cache: dict) -> Tuple[float, dict]:
        grads = {}
        loss, dOut = self.criterion(X, y)
        dOut, grads["W%d" % self.num_layers] = linear_backward(dOut, cache['linear%d' % self.num_layers])

        for i in range(self.num_layers - 2, -1, -1):
            dOut = relu_backward(dOut, cache['relu%d' % (i + 1)])
            dOut, grads['W%d' % (i + 1)], grads['b%d' % (i + 1)] = linear_backward(dOut, cache['linear%d' % (i + 1)])

        return loss, grads

    def predict(self, X: np.ndarray):
        Z, _ = self.forward(X)
        return self.output_activation(Z[-1])


if __name__ == '__main__':
    ...
