from typing import Tuple, List
import albumentations as A
import numpy as np
import torch
import os
import cv2
from torch import nn
from tqdm import tqdm
from albumentations.pytorch.transforms import ToTensorV2
labels2names ={
  "0": "alpha",
  "1": "beta",
  "2": "eta",
  "3": "kappa",
  "4": "lambda",
  "5": "nu",
  "6": "phi",
  "7": "pi",
  "8": "sigma",
  "9": "tau"
}
def read_images(image_dir_path: str, labels2names: dict = None) -> Tuple[List[np.ndarray], List[int], dict]:
    names2labels = None
    if labels2names is None:
        labels2names = {}
    else:
        names2labels = {v: k for k, v in labels2names.items()}
    labels = []
    images = []

    for i, img_dir in enumerate(os.listdir(image_dir_path)):
        if names2labels is None:
            labels2names[i] = img_dir
        for img in os.listdir(os.path.join(image_dir_path, img_dir)):
            image = cv2.cvtColor(cv2.imread(os.path.join(image_dir_path, img_dir, img)), cv2.COLOR_BGR2GRAY)
            image[image <= 98] = 1
            image[image > 98] = 0
            images.append(crop_borders(image))
            if names2labels is not None:
                labels.append(names2labels[img_dir])
            else:
                labels.append(i)

    return images, labels, labels2names


def crop_borders(image: np.ndarray) -> np.ndarray:
    try:
        mask = image == 0

        coords = np.array(np.nonzero(~mask))
        top_left = np.min(coords, axis=1)
        bottom_right = np.max(coords, axis=1)

        out = image[top_left[0] - 5:bottom_right[0] + 5, top_left[1] - 5:bottom_right[1] + 5]
        if out.shape[0] == 0 or out.shape[1] == 0:
            center_y, center_x = image.shape[0] // 2, image.shape[1] // 2
            return image[center_y - center_y // 2:center_y + center_y // 2,
                   center_x - center_x // 2: center_x + center_x // 2]

        return out
    except Exception:
        return image


class ImageDataset(torch.utils.data.Dataset):
    def __init__(self, image_dir_path: str = './data', dataset_len: int = 3000, labels2names: dict = None):
        images, labels, labels2names = read_images(image_dir_path, labels2names)
        self.images = images
        self.labels = labels
        self.labels2names = labels2names
        self.transform = A.Compose([
            A.Downscale(p=0.3),
            A.GaussianBlur(p=0.5),
            A.Rotate(limit=15, p=0.6, border_mode=cv2.BORDER_CONSTANT, value=0),
            A.Resize(400, 400),
            ToTensorV2(p=1.0)
        ])
        self.dataset_len = dataset_len

    def __len__(self):
        return self.dataset_len

    def __getitem__(self, idx: int):
        idx = idx % len(self.labels)
        image = self.transform(image=self.images[idx])["image"]

        return image.float(), self.labels[idx]

    @property
    def labels2names_(self):
        return self.labels2names


class ClassificationConvNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.feature_extractor = torch.nn.Sequential(
            nn.Conv2d(1, 6, 5),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(6, 9, 5),
            nn.MaxPool2d(2, 2),

        )

        feature_extractor_output_shape = self.feature_extractor(
            torch.rand(1, 1, 400, 400)
        ).detach().shape

        feature_extractor_output_shape = feature_extractor_output_shape[1] * \
                                         feature_extractor_output_shape[2] * \
                                         feature_extractor_output_shape[3]

        self.classification_head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(feature_extractor_output_shape, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        x = self.feature_extractor(x)
        return self.classification_head(x)


if __name__ == '__main__':
    ## inits
    net = ClassificationConvNet()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=1e-4, weight_decay=0.001)
    output_activation = torch.nn.Softmax(dim=1)

    ## data
    traindataset = ImageDataset(dataset_len=5000)
    labels2names = traindataset.labels2names_
    trainloader = torch.utils.data.DataLoader(
        traindataset, batch_size=50, shuffle=True, num_workers=2
    )

    testloader = torch.utils.data.DataLoader(
        ImageDataset(dataset_len=500, labels2names=labels2names),
        batch_size=50, shuffle=True, num_workers=2
    )
    valloader = torch.utils.data.DataLoader(
        ImageDataset(dataset_len=500, labels2names=labels2names),
        batch_size=50, shuffle=True, num_workers=2
    )
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    net.to(device)
    ## training loop
    num_epochs = 3
    for epoch in range(num_epochs):
        running_loss = 0
        running_accuracy = 0
        i = 0
        for data in tqdm(trainloader):
            x, y = data[0].to(device), data[1].to(device)
            i += 1
            optimizer.zero_grad()
            outputs = net(x)
            preds = torch.argmax(output_activation(outputs), dim=1)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            running_accuracy += torch.mean((preds == y).float())

        val_running_accuracy = 0
        val_i = 0
        for data in tqdm(valloader):
            x, y = data[0].to(device), data[1].to(device)
            val_i += 1
            outputs = net(x)
            preds = torch.argmax(output_activation(outputs), dim=1)
            val_running_accuracy += torch.mean((preds == y).float())

        print("%d epoch:\n training loss: %.4f\n " \
              "training accuracy: %.4f\n validation accuracy: %.4f" % (
                  epoch + 1, running_loss / i,
                  running_accuracy / i, val_running_accuracy / val_i))
    PATH = '../TelegramBot/GREEK_net.pth'
    torch.save(net.state_dict(), PATH)
