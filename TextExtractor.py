import cv2
import numpy as np
#import ValidateDictionary
#import east

class ImageLabel:
    def __init__(self, image, coordinates):
        self.image = image
        self.coordinates = coordinates

def image_thresholding(img, thresh):
    # load image
    image = img
    # resize image
    image = cv2.resize(image,None,fx=5, fy=5, interpolation = cv2.INTER_CUBIC)
    # create grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # perform threshold
    _, mask = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)
    # find contours
    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # draw black over the contours smaller than 200 - remove unwanted blobs
    for cnt in contours:
        # print contoursize to detemine threshold
        print(cv2.contourArea(cnt))
        if cv2.contourArea(cnt) < 200:
            cv2.drawContours(mask, [cnt], 0, (0), -1)
    return image

def clip_labels(images):
    for img in images:
        pass
        

class TextExtractor:
    def __init__(self, images):
        self.images = images
        pass
        #run EAST
        #run image_thresholding for each coordinate
        