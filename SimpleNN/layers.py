import numpy as np


def linear_backward(d: np.ndarray, prev: tuple):
    X, W, b = prev
    dX = np.dot(d, W.T).reshape(X.shape)
    dW = np.dot(X.reshape(-1, W.shape[0]).T, d)
    db = d.sum(0)

    return dX, dW, db


def linear(X: np.ndarray, W: np.ndarray, b: np.ndarray):
    return np.dot(X, W) + b, (X, W, b)


def sigmoid(X: np.ndarray):
    return 1 / (1 + np.exp(-X))


def sigmoid_backward(d: np.ndarray, prev: np.ndarray):
    X = prev.copy()
    sigma = sigmoid(X)
    return sigma * (1 - sigma) * d


def relu_backward(d: np.ndarray, prev: np.ndarray):
    X = prev.copy()
    dx = d.copy()
    dx[X <= 0] = 0
    return dx


def relu(X: np.ndarray):
    return np.maximum(0, X), X


def softmax(X: np.ndarray):
    e_x = np.exp(X - np.max(X))
    return e_x / np.sum(np.exp(e_x), axis=1, keepdims=True)


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


def mse_loss(X: np.ndarray, y: np.ndarray):
    preds = sigmoid(X)
    y_encoded = np.zeros((y.shape[0], y.max(initial=0) + 1))
    y_encoded[np.arange(y.shape[0]), y] = 1
    loss = np.mean((y_encoded - preds) ** 2)
    N = X.shape[0]
    dX = sigmoid_backward(X, 2 * (preds - y_encoded))
    return loss, dX
