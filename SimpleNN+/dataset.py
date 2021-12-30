from typing import Tuple, List, Union

import albumentations as A
import numpy as np
import torch
import os
import cv2
import numba


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


@numba.jit(nopython=True)
def compute_sample(image: np.ndarray) -> List[Union[int, np.ndarray]]:
    cell_width, cell_height = 20, 20
    return [np.sum(image[i * cell_height:(i + 1) * cell_height,
                   j * cell_width:(j + 1) * cell_width])
            for i in range(image.shape[0] // cell_height)
            for j in range(image.shape[1] // cell_width)]

@numba.jit(nopython=True)
def compute_new_sample(image:np.ndarray) -> List[Union[int, np.ndarray]]:
    cell_width, cell_height = 2, 2
    result = [np.sum(image[i*cell_height, :]) for i in range(image.shape[0] // cell_height )]
    result.extend([np.sum(image[:, j * cell_width]) for j in range(image.shape[0] // cell_width )])
    return result



class ImageDataset(torch.utils.data.Dataset):
    def __init__(self, image_dir_path: str = './data', dataset_len: int = 3000, labels2names: dict = None):
        images, labels, labels2names = read_images(image_dir_path, labels2names)
        self.images = images
        self.labels = labels
        self.labels2names = labels2names
        self.transform = A.Compose([
            A.Downscale(p=0.3),
            A.GlassBlur(p=0.3),
            A.GaussianBlur(p=0.3),
            A.Resize(400, 400)
        ])
        self.dataset_len = dataset_len

    def __len__(self):
        return self.dataset_len

    def __getitem__(self, idx: int):
        idx = idx % len(self.labels)
        image = self.transform(image=self.images[idx])["image"]
        # cv2.imshow("", (image * 255))
        # cv2.waitKey()
        return compute_new_sample(image), self.labels[idx]

    @property
    def labels2names_(self):
        return self.labels2names


if __name__ == "__main__":
    dataset = ImageDataset(dataset_len=600)
    print(dataset.labels2names_)

    # for i in range(len(dataset)):
    #     x, y = dataset[i]
    #     print(len(x))
