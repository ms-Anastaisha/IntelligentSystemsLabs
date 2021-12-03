import numpy as np
from typing import Tuple
from layers import (linear, linear_backward, relu, relu_backward,
                    mse_loss, sigmoid, softmax_loss,
                    softmax)
from optimizers import Optimizer
from tqdm import tqdm, trange


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

        self.loss_history = []

    def check_accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        pass

    def _training_step(self, X_batch: np.ndarray, y_batch: np.ndarray, optimizer: Optimizer):
        _, caches = self.forward(X_batch)
        loss, grads = self.backward(X_batch, y_batch, caches)
        self.loss_history.append(loss)
        for key, weight in self.params.items():
            grads[key] = optimizer(weight, grads[key])

    def check_accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        preds = self.predict(X)

        return np.mean(preds == y)

    def train(self, X: np.ndarray, y: np.ndarray,
              X_val: np.ndarray, y_val: np.ndarray,
              optimizer: Optimizer = Optimizer(), acc_thresh: float = 0.98,
              num_epochs: int = 10, batch_size=50):
        best_params = {}
        best_val_acc = 0
        for num_epoch in trange(num_epochs):
            batch_cnt = X.shape[0] // batch_size

            for i in range(batch_cnt + 1):
                X_batch, y_batch = X[i * batch_size: (i + 1) * batch_size], y[i * batch_size: (i + 1) * batch_size]
                self._training_step(X_batch, y_batch, optimizer)
            print("Training loss after %d epoch: %d" % (num_epoch + 1, self.loss_history[-1]))

            _, caches = self.forward(X_val)
            loss, _ = self.backward(X_val, y_val, caches)
            print("Validation loss after %d epoch: %d" % (num_epoch + 1, self.loss_history[-1]))
            self.loss_history = []
            train_acc = self.check_accuracy(X, y)
            val_acc = self.check_accuracy(X_val, y_val)

            print("Training accuracy after %d epoch: %d" % (num_epoch + 1, train_acc))
            print("Validation loss after %d epoch: %d" % (num_epoch + 1, val_acc))

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_params = self.params

            if best_val_acc > acc_thresh:
                break
        self.params = best_params

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
