from typing import Tuple, List

import albumentations as A
import numpy as np
import torch
import os
import cv2


# Downscale, GaussianBlur, GaussNoise, RandomScale
def read_images(image_dir_path: str) -> Tuple[List[np.ndarray], List[int], dict]:
    labels2names = {}
    labels = []
    images = []

    for i, img_dir in enumerate(os.listdir(image_dir_path)):
        labels2names[i] = img_dir
        for img in os.listdir(os.path.join(image_dir_path, img_dir)):
            image = cv2.cvtColor(cv2.imread(os.path.join(image_dir_path, img_dir, img)), cv2.COLOR_BGR2GRAY)
            image[image <= 98] = 1
            image[image > 98] = 0
            images.append(crop_borders(image))
            labels.append(i)

    return images, labels, labels2names


def crop_borders(image):
    mask = image == 0

    coords = np.array(np.nonzero(~mask))
    top_left = np.min(coords, axis=1)
    bottom_right = np.max(coords, axis=1)

    out = image[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]

    return out


class ImageDataset(torch.utils.data.Dataset):
    def __init__(self, image_dir_path: str = './data', dataset_len: int = 3000):
        self.images, self.labels, self.labels2names = read_images(image_dir_path)
        self.transform = A.Compose([
            A.Downscale(p=0.3),
            A.GlassBlur(p=0.3),
            A.GaussNoise(p=0.3),
            A.GaussianBlur(p=0.3),
            A.Rotate(limit=10, p=0.4),
            A.RandomScale(p=0.4),
            A.Resize(400, 400)
        ])
        self.dataset_len = dataset_len

    def __len__(self):
        return self.dataset_len

    def __getitem__(self, idx: int):
        idx = idx % len(self.labels)


if __name__ == "__main__":
    read_images('./data')
