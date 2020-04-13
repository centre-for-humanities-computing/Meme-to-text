import cv2
import numpy as np
import tempfile
import pytesseract

def order_boxes(boxes):
    ''' method that orders boxes in a left-to-right, top-to-bottom
        approach. This has it's faults when it comes to memes,
        but generally is a safe-approach.
    '''
    boxes.sort(key=lambda b: b[1])
    # initially the line bottom is set to be the bottom of the first rect
    line_bottom = boxes[0][1]+boxes[0][3]-1
    line_begin_idx = 0
    for i in range(len(boxes)):
        # when a new box's top is below current line's bottom
        # it's a new line
        if boxes[i][1] > line_bottom:
            # sort the previous line by their x
            boxes[line_begin_idx:i] = sorted(boxes[line_begin_idx:i], key=lambda b: b[0])
            line_begin_idx = i
        # regardless if it's a new line or not
        # always update the line bottom
        line_bottom = max(boxes[i][1]+boxes[i][3]-1, line_bottom)
    # sort the last line
    boxes[line_begin_idx:] = sorted(boxes[line_begin_idx:], key=lambda b: b[0])
    return boxes

def get_contours(img, inverted=False):
    # Invert the image
    if inverted:
        img = cv2.bitwise_not(img)
    # Convert the image to gray scale 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
    cv2.imwrite("thresh1.png", thresh1)  
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 

    # Appplying dilation on the threshold image 
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
    
    # Finding contours 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,  
                                                    cv2.CHAIN_APPROX_NONE)
    bounding_rectangles = []
    #Sort rectangles
    for cnt in contours: 
        (x, y, w, h) = cv2.boundingRect(cnt)
        bounding_rectangles.append((x, y, w, h))
    bounding_rectangles = order_boxes(bounding_rectangles)
    return bounding_rectangles

def extractText(img):
    image = cv2.imread(img) 
    im2 = image.copy() 
    bounding_rectangles = get_contours(image)
    bounding_rectangles += get_contours(image, inverted=True)
    ocr_text = ""
    for rect in bounding_rectangles:
        (x, y, w, h) = rect
        # Cropping the text block for giving input to OCR 
        cropped = im2[y:y + h, x:x + w] 
        # Apply OCR on the cropped image 
        text = pytesseract.image_to_string(cropped)
        # Appending the text into file 
        if len(text) > 1:
            ocr_text += text + "\n"
    return ocr_text

class TextExtractor:
    def __init__(self):
        self.images = []
    def extract_text(self, images):
        for img in images:
            img_str = img._str
            if '.ds_store' in img_str.lower():
                continue
            text = extractText(img_str)
            self.images.append(ImageLabel(img, text))
        return self.images

class ImageLabel:
    def __init__(self, image, ocr):
        self.image = image
        self.ocr = ocr
    def save_to(self, output_dir=""):
        output = output_dir + self.image.stem
        with open(output, "w+") as f:
            print("Writing file {}".format(self.image.stem))
            f.write(self.ocr)