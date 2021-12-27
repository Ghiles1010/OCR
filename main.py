import os
import cv2
import numpy as np
from copy import deepcopy
from ui import UI

PATH = "images"
WINDOW_NAME = "result"


def gray_scale(image, x=None):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)


def threshold(image, x):
    # has to return bgr format nor gray scale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.threshold(image, x, 255, 0, image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image


def mean_blur(image, x):
    if x == 0: x = 1
    kernel = np.ones((x, x), np.float32) / x ** 2
    return cv2.filter2D(image, -1, kernel)


# def load_images():
#     return [cv2.imread(os.path.join(PATH, file)) for file in os.listdir(PATH)]


def test():
    # img = cv2.imread("images/image3.jpg")
    img  = np.zeros((600,600,3), dtype=np.uint8)
    img.shape
    print(img.shape)
    res = threshold(img, 125)
    cv2.imshow("", res)
    cv2.waitKey(0)

def main():

    # test()

    ui = UI()
    
    ui.add_filter("Binarization", threshold, "threshold", 0, 255, 125)


    ui.add_filter("Mean Blur", mean_blur, "voisinage", 1, 10, 7)
    ui.add_filter("Mean Blur", mean_blur, "voisinage", 1, 10, 7)
    
    ui.show()
    


if __name__ == '__main__':
    main()
