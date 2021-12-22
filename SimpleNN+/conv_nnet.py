from collections import OrderedDict

import torch
from torch import nn

class View(nn.Module):
    def __init__(self):


class ClassificationConvNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = torch.nn.Sequential(
            nn.Conv2d(3, 6, 5),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(6, 16, 5),
            nn.MaxPool2d(2, 2),
           )
