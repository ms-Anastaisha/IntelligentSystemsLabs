import numpy as np


class Optimizer:
    def __init__(self, optim_type: str = 'sgd', params: dict = None):
        if params is None:
            self.params = {}
        else:
            self.params = params
        self.params.setdefault('lr', 1e-3)

        if optim_type == 'sgd':
            self.optimize = self.sgd
        elif optim_type == 'momentum':
            self.optimize = self.nesterov_momentum
        elif optim_type == 'adam':
            self.optimize = self.adam
        elif optim_type == 'nadam':
            self.optimize = self.nadam

    def __call__(self, W: np.ndarray, dW: np.ndarray):
        self.optimize(W, dW)

    def sgd(self, W: np.ndarray, dW: np.ndarray) -> np.ndarray:
        W -= self.params['lr'] * dW
        return W

    def nesterov_momentum(self, W: np.ndarray, dW: np.ndarray) -> np.ndarray:
        pass

    def adam(self, W: np.ndarray, dW: np.ndarray, params=None) -> np.ndarray:
        pass

    def nadam(self, W: np.ndarray, dW: np.ndarray) -> np.ndarray:
        pass
