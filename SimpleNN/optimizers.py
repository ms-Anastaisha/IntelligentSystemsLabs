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

    def adam(self, W: np.ndarray, dW: np.ndarray, key:str) -> np.ndarray:
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
