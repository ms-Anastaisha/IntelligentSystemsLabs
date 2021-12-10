import numpy as np
from typing import Tuple

import torch
from tqdm import trange

from dataset import ImageDataset


def linear_backward(d: np.ndarray, prev: tuple):
    X, W, b = prev
    dX = np.dot(d, W.T).reshape(X.shape)
    dW = np.dot(X.reshape(-1, W.shape[0]).T, d)
    db = d.sum(0)

    return dX, dW, db


def linear(X: np.ndarray, W: np.ndarray, b: np.ndarray):
    return np.dot(X, W) + b, (X, W, b)


def relu_backward(d: np.ndarray, prev: np.ndarray):
    X = prev.copy()
    dx = d.copy()
    dx[X <= 0] = 0
    return dx


def relu(X: np.ndarray):
    return np.maximum(0, X), X


def softmax(X: np.ndarray):
    e_x = np.exp(X - np.max(X))
    if len(e_x.shape) > 1:
        return e_x / np.sum(e_x, axis=1, keepdims=True)
    return e_x / np.sum(e_x)


def softmax_loss(X: np.ndarray, y: np.ndarray):
    logits = X - np.max(X, axis=1, keepdims=True)
    Z = np.sum(np.exp(logits), axis=1, keepdims=True)
    log_probs = logits - np.log(Z)
    probs = np.exp(log_probs)
    N = X.shape[0]
    loss = -np.sum(log_probs[np.arange(N), y]) / N
    dX = probs.copy()
    dX[np.arange(N), y] -= 1
    dX /= N
    return loss, dX


class Optimizer:
    def __init__(self, optim_type: str = 'sgd', params: dict = None):
        if params is None:
            self.params = {}
        else:
            self.params = params
        self.params.setdefault('lr', 1e-3)
        self.params.setdefault('momentum', 0.9)
        self.params.setdefault("beta1", 0.9)
        self.params.setdefault("beta2", 0.999)

        if optim_type == 'sgd':
            self.optimize = self.sgd
        elif optim_type == 'momentum':
            self.optimize = self.momentum
        elif optim_type == 'adam':
            self.optimize = self.adam

    def __call__(self, W: np.ndarray, dW: np.ndarray, key: str):
        return self.optimize(W, dW, key)

    def sgd(self, W: np.ndarray, dW: np.ndarray, key: str) -> np.ndarray:
        W -= self.params['lr'] * dW
        return W

    def momentum(self, W: np.ndarray, dW: np.ndarray, key: str) -> np.ndarray:
        v = self.params.get("velocity %s" % key, np.zeros_like(W))
        v = self.params["momentum"] * v + self.params["lr"] * dW
        W -= v
        self.params["velocity %s" % key] = v
        return W

    def adam(self, W: np.ndarray, dW: np.ndarray, key: str) -> np.ndarray:
        m = self.params.get("m %s" % key, np.zeros_like(W))
        v = self.params.get("v %s" % key, np.zeros_like(W))
        self.params.setdefault("t %s" % key, 0)
        self.params['t %s' % key] += 1
        self.params['m %s' % key] = self.params["beta1"] * m + (1 - self.params["beta1"]) * dW
        self.params['v %s' % key] = self.params["beta2"] * v + (1 - self.params["beta2"]) * dW ** 2
        mt = self.params['m %s' % key] / (1 - np.power(self.params["beta1"], self.params["t %s" % key]))
        vt = self.params["v %s" % key] / (1 - np.power(self.params["beta2"], self.params["t %s" % key]))
        W -= self.params["lr"] * mt / (np.sqrt(vt) + 1e-8)
        return W


class NNet:

    def __init__(self, hidden_dims: list = [500], num_cls: int = 10,
                 input_dim: int = 400):
        ## architecture
        self.params = {}
        std = 1e-4
        self.params['W1'] = std * np.random.randn(input_dim, hidden_dims[0])
        self.params['b1'] = np.zeros(hidden_dims[0])
        for i in range(1, len(hidden_dims)):
            self.params['W%d' % (i + 1)] = std * np.random.randn(hidden_dims[i - 1], hidden_dims[i])
            self.params['b%d' % (i + 1)] = np.zeros(hidden_dims[i])
        self.params['W%d' % (len(hidden_dims) + 1)] = std * np.random.randn(hidden_dims[-1], num_cls)
        self.params['b%d' % (len(hidden_dims) + 1)] = np.zeros(num_cls)
        self.num_layers = len(hidden_dims) + 1

        ## params
        self.output_activation = softmax
        self.criterion = softmax_loss
        self.optimizer = Optimizer("adam")
        self.loss_history = []

        ## datasets
        traindataset = ImageDataset(dataset_len=3000)
        self.labels2names = traindataset.labels2names_
        self.trainloader = torch.utils.data.DataLoader(
            traindataset, batch_size=50, shuffle=True, num_workers=2
        )

        self.testloader = torch.utils.data.DataLoader(
            ImageDataset(dataset_len=300, labels2names=self.labels2names),
            batch_size=50, shuffle=True, num_workers=2
        )
        self.valloader = torch.utils.data.DataLoader(
            ImageDataset(dataset_len=300, labels2names=self.labels2names),
            batch_size=50, shuffle=True, num_workers=2
        )

    def _training_step(self, X_batch: np.ndarray, y_batch: np.ndarray, optimizer: Optimizer):
        Z, caches = self.forward(X_batch)
        loss, grads = self.backward(Z[-1], y_batch, caches)
        self.loss_history.append(loss)
        for key, weight in self.params.items():
            self.params[key] = optimizer(weight, grads[key], key)

    def check_accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        preds = self._predict(X)
        preds = np.argmax(preds, axis=1)
        return np.mean(preds == y)

    def train(self, num_epochs: int = 10):
        best_params = {}
        best_val_acc = -1
        for num_epoch in trange(num_epochs):
            running_accuracy = 0
            i = 0
            for data in self.trainloader:
                X_batch, y_batch = data
                self._training_step(X_batch, y_batch, self.optimizer)
                running_accuracy += self.check_accuracy(X_batch, y_batch)
                i += 1
            training_loss = np.mean(self.loss_history)
            train_acc = running_accuracy / i

            ## validation
            X_val, y_val = [], []
            for data in self.valloader:
                X_val_batch, y_val_batch = data
                X_val.extend(X_val_batch)
                y_val.extend(y_val_batch)
            X_val, y_val = np.array(X_val), np.array(y_val)
            Z, caches = self.forward(X_val)
            loss, _ = self.backward(Z[-1], y_val, caches)
            val_acc = self.check_accuracy(X_val, y_val)

            self.loss_history = []

            yield "%d epoch:\n training loss: %.4f\n " \
                  "training accuracy: %.4f\n validation accuracy: %.4f" % (num_epoch + 1,
                                                                           training_loss,
                                                                           train_acc, val_acc)
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_params = self.params

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
        dOut, grads["W%d" % self.num_layers], grads["b%d" % self.num_layers] = linear_backward(dOut, cache[
            'linear%d' % self.num_layers])

        for i in range(self.num_layers - 2, -1, -1):
            dOut = relu_backward(dOut, cache['relu%d' % (i + 1)])
            dOut, grads['W%d' % (i + 1)], grads['b%d' % (i + 1)] = linear_backward(dOut, cache['linear%d' % (i + 1)])

        return loss, grads

    def _predict(self, X: np.ndarray):
        Z, _ = self.forward(X)
        return self.output_activation(Z[-1])

    def predict(self, X: np.ndarray):
        prediction = self._predict(X)
        label = np.argmax(prediction)
        predictions = []
        for i, p in enumerate(prediction):
            predictions.append("%s : %.5f" % (self.labels2names[i], p))

        return "Prediction: %s \nProbabilities:\n%s" % (self.labels2names[label],
                                                        "\n".join(predictions))

    def test(self):
        running_accuracy = 0
        i = 0
        for data in self.testloader:
            x, y = data
            i += 1
            running_accuracy += self.check_accuracy(x, y)

        return "Test accuracy: %.4f" % (running_accuracy / i)


if __name__ == '__main__':
    ...
    # model = NNet(hidden_dims=[500, 20],
    #              num_cls=4, loss='mse')
    # optimizer = Optimizer('adam')
    # samples_per_class = 2000
    # X_train, y_train = dt.create_dataset(4, int(samples_per_class * 0.9))
    # X_val, y_val = dt.create_dataset(4, int(samples_per_class * 0.1))
    # model.train(X_train, y_train, X_val, y_val, optimizer, num_epochs=10)
    # generate_funcs = [dt.create_random_rectangle, dt.create_random_triangle,
    #                   dt.create_random_circle, dt.create_random_sine]
    # figure_num = np.random.choice(1000) % 4
    # figure = generate_funcs[figure_num]()
    # print(figure_num)
    # horizontal = np.sum(figure, axis=1)
    # vertical = np.sum(figure, axis=0)
    # fig_vec = np.append(horizontal, vertical)
    # prediction = model.predict(fig_vec)
    # print(prediction)
