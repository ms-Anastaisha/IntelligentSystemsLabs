import cv2
import numpy as np
import warnings

warnings.filterwarnings("ignore")
from tqdm import trange

WIDTH = 200
HEIGHT = 200


def create_random_circle():
    canvas = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
    radius = np.random.choice(np.arange(10, 75))
    x = np.random.choice(np.arange(radius + 5, WIDTH - radius - 5))
    y = np.random.choice(np.arange(radius + 5, HEIGHT - radius - 5))
    canvas = cv2.circle(canvas, (x, y), radius, 1, 1)
    return canvas


def create_random_rectangle():
    canvas = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
    w, h = np.random.choice(np.arange(10, 150), 2)
    x = np.random.choice(WIDTH - w - 5)
    y = np.random.choice(HEIGHT - h - 5)
    canvas = cv2.rectangle(canvas, (x, y), (x + w, y + h), 1, 1)
    return canvas


def adjust_points(p1, p2, threshold):
    if abs(p1 - p2) < threshold:
        if p1 > p2:
            p1 += threshold
        else:
            p2 += threshold
    return p1, p2


def create_random_triangle():
    canvas = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
    w1, w2, w3 = np.random.choice(np.arange(20, WIDTH - 20), 3)
    h1, h2 = np.random.choice(np.arange(20, HEIGHT - 20), 2)
    h1, h2 = adjust_points(h1, h2, 20)
    w2, w3 = adjust_points(w2, w3, 20)
    canvas = cv2.line(canvas, (w1, h1), (w2, h2), 1, 1)
    canvas = cv2.line(canvas, (w1, h1), (w3, h2), 1, 1)
    canvas = cv2.line(canvas, (w2, h2), (w3, h2), 1, 1)
    return canvas


def create_random_sine():
    canvas = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
    x1 = np.random.choice(60) + 10
    x2 = np.random.choice(np.arange(x1 + 50, 190))
    x = np.arange(x1, x2, 5)
    height = np.random.choice(np.arange(20, 90))
    height_shift = height + np.random.choice(HEIGHT - height * 2)
    y = (np.sin(x) * height + height_shift).astype(int)
    for i in range(len(x) - 1):
        canvas = cv2.line(canvas, (x[i], y[i]), (x[i + 1], y[i + 1]), 1, 1);
    return canvas


def create_dataset(classCnt=2, samplesCnt=1000):
    figures, labels = [], []
    generate_funcs = [create_random_rectangle, create_random_triangle,
                      create_random_circle, create_random_sine]
    for i in range(classCnt):
        for _ in trange(samplesCnt):
            figure = generate_funcs[i]()
            horizontal = np.sum(figure, axis=1)
            vertical = np.sum(figure, axis=0)
            figures.append(np.append(horizontal, vertical))
        labels.extend([i] * samplesCnt)
    shuffle_mask = np.arange(len(figures))
    np.random.shuffle(shuffle_mask)
    figures, labels = np.array(figures)[shuffle_mask], np.array(labels)[shuffle_mask]
    return figures, labels


def label2class(label):
    classes = ["rectangle", "triangle", "circle", "sine"]
    return classes[label]


if __name__ == '__main__':
    """test"""
    dataset = create_dataset(4, 2000)
    print(dataset[0])
    print(dataset[2000])
    print(dataset[4000])
    print(dataset[6000])
