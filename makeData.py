import random

import cv2
import os

# from tqdm import tqdm
import numpy as np

INPUT_DIR = "realTest"
OUTPUT_DIR = "finalRealTrain"


def on_quit(used):
    with open("used.txt", 'a') as f:
        for i in used:
            f.write(i + ' ')


def on_load(used):
    with open("used.txt", 'r') as f:
        for i in f.readline().split():
            used.add(i)


def make_data(lim: int = 400):
    cur = int(input())
    files = os.listdir(INPUT_DIR)
    random.shuffle(files)
    used = set()
    on_load(used)
    for i, f in enumerate(files):
        if cur == lim:
            break
        if f in used:
            continue
        if (i + 1) % 50 == 0:
            print(f"{i + 1}-th image")
        try:
            img = cv2.resize(cv2.imread(os.path.join(INPUT_DIR, f)), (750, 750))
            cv2.imshow('image', img)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            c = int(input())
            if c == -1:
                break
            cv2.imwrite(os.path.join(OUTPUT_DIR, f"{cur}_{c}.jpg"), img)
            cur += 1
            used.add(f)
        except Exception as e:
            print(e)
    on_quit(used)


def remove_duplicates():
    files = os.listdir(OUTPUT_DIR)
    imgs = set()
    shape = (100, 100)
    for i, f in enumerate(sorted(files)):
        # if '_' not in f:
        #     os.remove(os.path.join(OUTPUT_DIR, f))
        #     continue
        img = cv2.resize(cv2.imread(os.path.join(OUTPUT_DIR, f), cv2.IMREAD_GRAYSCALE), (100, 100))
        shape = img.shape
        img = tuple(list(img.flatten()) + [int(f[-5])])
        # print(img)
        if img in imgs:
            continue
        imgs.add(img)
    print(len(imgs))
    for i, img in enumerate(imgs):
        img = list(img)
        val = img[-1]
        img.pop(len(img) - 1)
        img = np.array(img)
        img.resize(shape)
        try:
            cv2.imwrite(os.path.join("tmp", f"{i}_{val}.jpg"), img)
        except Exception as e:
            print(e)


def transfer():
    for f in sorted(os.listdir("tmp")):
        img = cv2.imread(os.path.join("tmp", f), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(os.path.join(OUTPUT_DIR, f), img)


def main():
    make_data()


if __name__ == '__main__':
    main()
