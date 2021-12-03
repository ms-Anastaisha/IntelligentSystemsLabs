import numpy as np
from typing import Tuple
from layers import (linear, linear_backward, relu, relu_backward,
                    mse_loss, sigmoid, softmax_loss,
                    softmax)
from optimizers import Optimizer
from tqdm import tqdm, trange
import dataset as dt

class NNet:

    def __init__(self, hidden_dims: list = [500], num_cls: int = 2,
                 input_dim: int = 400, std: float = 1e-4, loss: str = 'mse'):
        self.params = {}
        self.params['W1'] = std * np.random.randn(input_dim, hidden_dims[0])
        self.params['b1'] = np.zeros(hidden_dims[0])
        for i in range(1, len(hidden_dims) ):
            self.params['W%d' % (i + 1)] = std * np.random.randn(hidden_dims[i - 1], hidden_dims[i])
            self.params['b%d' % (i + 1)] = np.zeros(hidden_dims[i])
        self.params['W%d' % (len(hidden_dims) + 1)] = std * np.random.randn(hidden_dims[-1], num_cls)
        self.params['b%d' % (len(hidden_dims) + 1)] = np.zeros(num_cls)
        self.num_layers = len(hidden_dims) + 1
        if loss == 'mse':
            self.output_activation = sigmoid
            self.criterion = mse_loss
        else:
            self.output_activation = softmax
            self.criterion = softmax_loss

        self.loss_history = []

    def _training_step(self, X_batch: np.ndarray, y_batch: np.ndarray, optimizer: Optimizer):
        Z, caches = self.forward(X_batch)
        loss, grads = self.backward(Z[-1], y_batch, caches)
        self.loss_history.append(loss)
        for key, weight in self.params.items():
            self.params[key] = optimizer(weight, grads[key], key)

    def check_accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        preds = self.predict(X)

        return np.mean(preds == y)

    def train(self, X: np.ndarray, y: np.ndarray,
              X_val: np.ndarray, y_val: np.ndarray,
              optimizer: Optimizer = Optimizer(), acc_thresh: float = 0.98,
              num_epochs: int = 10, batch_size=50):
        best_params = {}
        best_val_acc = -1
        for num_epoch in trange(num_epochs):
            batch_cnt = X.shape[0] // batch_size

            for i in range(batch_cnt):
                X_batch, y_batch = X[i * batch_size: (i + 1) * batch_size], y[i * batch_size: (i + 1) * batch_size]
                self._training_step(X_batch, y_batch, optimizer)
            print(self.loss_history)
            print("Training loss after %d epoch: %.4f" % (num_epoch + 1, self.loss_history[-1]))

            Z, caches = self.forward(X_val)
            loss, _ = self.backward(Z[-1], y_val, caches)

            print("Validation loss after %d epoch: %.4f" % (num_epoch + 1, self.loss_history[-1]))
            self.loss_history = []
            train_acc = self.check_accuracy(X, y)
            val_acc = self.check_accuracy(X_val, y_val)

            print("Training accuracy after %d epoch: %.4f" % (num_epoch + 1, train_acc))
            print("Validation loss after %d epoch: %.4f" % (num_epoch + 1, val_acc))

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
            h, cache = relu(h)
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
        dOut, grads["W%d" % self.num_layers], grads["b%d" % self.num_layers] = linear_backward(dOut, cache['linear%d' % self.num_layers])

        for i in range(self.num_layers - 2, -1, -1):
            dOut = relu_backward(dOut, cache['relu%d' % (i + 1)])
            dOut, grads['W%d' % (i + 1)], grads['b%d' % (i + 1)] = linear_backward(dOut, cache['linear%d' % (i + 1)])

        return loss, grads

    def predict(self, X: np.ndarray):
        Z, _ = self.forward(X)
        return self.output_activation(Z[-1])


if __name__ == '__main__':
    model = NNet(hidden_dims=[100],
                 num_cls=2, loss='softmax')
    optimizer = Optimizer('adam')
    samples_per_class = 200
    X_train, y_train = dt.create_dataset(2, int(samples_per_class * 0.9))
    print(X_train.shape, y_train.shape)
    X_val, y_val = dt.create_dataset(2, int(samples_per_class * 0.1))
    model.train(X_train, y_train, X_val, y_val, optimizer, num_epochs=5)
    generate_funcs = [dt.create_random_rectangle, dt.create_random_triangle,
                      dt.create_random_circle, dt.create_random_sine]
    figure_num = np.random.choice(1000) % 2
    figure = generate_funcs[figure_num]()
    horizontal = np.sum(figure, axis=1)
    vertical = np.sum(figure, axis=0)
    fig_vec = np.append(horizontal, vertical)
    prediction = model.predict(fig_vec)
    print(prediction)
