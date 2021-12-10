from collections import OrderedDict

import torch

from dataset import ImageDataset


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

        def train(self, num_epochs: int = 10):
            criterion = torch.nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(self.net.parameters(), lr=0.001)

            for epoch in range(num_epochs):
                running_loss = 0
                running_accuracy = 0
                i = 0
                for data in self.trainloader:
                    x, y = data
                    i += 1

                    optimizer.zero_grad()

                    outputs = self.net(x)
                    preds = torch.argmax(self.output_activation(outputs), dim=1)
                    loss = criterion(outputs, y)
                    loss.backward()
                    optimizer.step()
                    running_loss += loss.item()
                    running_accuracy += torch.mean(preds == y)

                val_running_accuracy = 0
                val_i = 0
                for data in self.valloader:
                    x, y = data
                    val_i += 1

                    outputs = self.net(x)
                    preds = torch.argmax(self.output_activation(outputs), dim=1)
                    val_running_accuracy += torch.mean(preds == y)

                yield "%d epoch:\n training loss: %.4f\n " \
                      "training accuracy: %.4f\n validation accuracy: %.4f" % (
                          epoch + 1, running_loss / i,
                          running_accuracy / i, val_running_accuracy / val_i)

        def predict(self, x):
            prediction = self.output_activation(self.net(x))
            label = torch.argmax(prediction)
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

                outputs = self.net(x)
                preds = torch.argmax(self.output_activation(outputs), dim=1)
                running_accuracy += torch.mean(preds == y)

            return "Test accuracy: %.4f" % (running_accuracy / i)
