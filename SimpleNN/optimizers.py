import numpy as np


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
        self.params.setdefault("t", 0)

        if optim_type == 'sgd':
            self.optimize = self.sgd
        elif optim_type == 'momentum':
            self.optimize = self.momentum
        elif optim_type == 'adam':
            self.optimize = self.adam

    def __call__(self, W: np.ndarray, dW: np.ndarray):
        self.optimize(W, dW)

    def sgd(self, W: np.ndarray, dW: np.ndarray) -> np.ndarray:
        W -= self.params['lr'] * dW
        return W

    def momentum(self, W: np.ndarray, dW: np.ndarray) -> np.ndarray:
        v = self.params.get("velocity", np.zeros_like(W))
        v = self.params["momentum"] * v + self.params["lr"] * dW
        W -= v
        self.params["velocity"] = v
        return W

    def adam(self, W: np.ndarray, dW: np.ndarray) -> np.ndarray:
        m = self.params.get("m", np.zeros_like(W))
        v = self.params.get("v", np.zeros_like(W))
        self.params['t'] += 1
        self.params['m'] = self.params["beta1"] * m + (1 - self.params["beta1"]) * dW
        self.params['v'] = self.params["beta2"] * v + (1 - self.params["beta2"]) * dW ** 2
        mt = self.params['m'] / (1 - np.power(self.params["beta1"], self.params["t"]))
        vt = self.params["v"] / (1 - np.power(self.params["beta2"], self.params["t"]))
        W -= self.params["lr"] * mt / (np.sqrt(vt) + 1e-8)
        return W