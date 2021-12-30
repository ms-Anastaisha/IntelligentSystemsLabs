from collections import OrderedDict
from typing import Tuple, List, Union

import torch
from torch import nn
import numpy as np
import numba

from tqdm import tqdm

labels2names = {
    0: "alpha",
    1: "beta",
    2: "eta",
    3: "kappa",
    4: "lambda",
    5: "nu",
    6: "phi",
    7: "pi",
    8: "sigma",
    9: "tau"
}


@numba.jit(nopython=True)
def compute_new_sample(image: np.ndarray) -> List[Union[int, np.ndarray]]:
    cell_width, cell_height = 2, 2
    result = [np.sum(image[i * cell_height, :]) for i in range(image.shape[0] // cell_height)]
    result.extend([np.sum(image[:, j * cell_width]) for j in range(image.shape[0] // cell_width)])
    return result




class ClassificationNet(torch.nn.Module):
    def __init__(self, hidden_dims: list = [500], num_cls: int = 10,
                 input_dim: int = 400):
        super().__init__()
        architecture = OrderedDict()
        architecture["linear_1"] = torch.nn.Linear(input_dim, hidden_dims[0])
        architecture["relu_1"] = torch.nn.ReLU()
        for i in range(1, len(hidden_dims)):
            architecture['linear_%d' % (i + 1)] = torch.nn.Linear(hidden_dims[i - 1], hidden_dims[i])
            architecture['relu_%d' % (i + 1)] = torch.nn.ReLU()
        architecture['linear_%d' % (len(hidden_dims) + 1)] = torch.nn.Linear(hidden_dims[-1], num_cls)
        self.net = torch.nn.Sequential(architecture)

    def forward(self, x):
        return self.net(x)
