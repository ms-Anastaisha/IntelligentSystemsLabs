from collections import OrderedDict

import torch


class Dataset:
    ...


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


class NetWrapper:
    def __init__(self, architecture):
        self.net = ClassificationNet(architecture)

        self.output_activation = torch.nn.Softmax(dim=1)
        self.criterion = torch.nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=0.001)

    def train(self, num_epochs: int = 10):
        ...

    def predict(self):
        ...
