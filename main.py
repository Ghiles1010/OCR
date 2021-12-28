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

def otsu_binarisation(image, x):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU, image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image.copy()

def mean_blur(image, x):
    return cv2.blur(image, (x, x))

def gaussian_blur(image, x):
    return cv2.GaussianBlur(image, (x, x), 3)

def median_blur(image, x):
    if x%2 == 0 : x+=1
    return cv2.medianBlur(image.astype(np.uint8), x)

def billateral_filter(image, x):
    return cv2.bilateralFilter(image.astype(np.uint8), x, 75, 75)

def erode(image, x):
    if x%2 == 0 : x+=1
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (x, x))
    return cv2.erode(image, kernel, iterations = 1)

def dilate(image, x):
    if x%2 == 0 : x+=1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (x, x))
    return cv2.dilate(image, kernel, iterations = 1)


def adaptive_Gaussian_binarisation(image, x):
    if x%2 == 0 : x+=1
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, x, 2)
    return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

def adaptive_mean_binarisation(image, x):
    if x%2 == 0 : x+=1
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, x, 2)
    return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)





def test():
    img = cv2.imread("images/image3.jpg")

    res = otsu_binarisation(img, 125)
    cv2.imshow("", res)
    cv2.waitKey(0)

def main():

    # test()

    ui = UI()
    
    ui.add_filter("Binarisation", threshold, "threshold", 0, 255, 125)
    ui.add_filter("Mean Blur", mean_blur, "voisinage", 1, 50, 1)
    ui.add_filter("Median Blur", median_blur, "size", 1, 50, 1)
    ui.add_filter("GaussianBlur", mean_blur, "size", 1, 50, 1)
    ui.add_filter("Billateral", billateral_filter, "size", 1, 20, 1)
    ui.add_filter("Erode", erode, "size", 1, 50, 1)
    ui.add_filter("Dilate", dilate, "size", 1, 50, 1)


    ui.add_filter("Adaptive Gaussian Binarisation", adaptive_Gaussian_binarisation, "size", 2, 200, 3)
    ui.add_filter("Adaptive Mean Binarisation", adaptive_mean_binarisation, "size", 2, 200, 3)
    ui.add_filter("Otsu's Binarisation", otsu_binarisation, "size", 2, 50, 3)



    
    ui.show()
    


if __name__ == '__main__':
    main()
