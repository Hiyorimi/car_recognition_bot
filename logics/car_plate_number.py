import numpy as np
import cv2
import matplotlib.pyplot as plt
import pytesseract


carplate_haar_cascade = cv2.CascadeClassifier('./haarcascade_russian_plate_number.xml')


# Create function to retrieve only the car plate region itself
def carplate_extract(image):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    carplate_img= None
    for x, y, w, h in carplate_rects:
        carplate_img = image[y + 15:y + h - 10,
                       x + 15:x + w - 20]  # Adjusted to extract specific region of interest i.e. car license plate

    return carplate_img


# Enlarge image for further processing later on
def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image


def prepare_image_for_ocr(img):
    carplate_extract_img = carplate_extract(img)
    carplate_extract_img = enlarge_img(carplate_extract_img, 150)
    carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
    carplate_extract_img_gray_blur = cv2.medianBlur(carplate_extract_img_gray, 3)  # kernel size 3

    return carplate_extract_img_gray_blur


def extract_plate_number(img) -> str:
    carplate_extract_img_gray_blur = prepare_image_for_ocr(img)
    recognized_number = pytesseract.image_to_string(
        carplate_extract_img_gray_blur,
        config=f'--psm 9 --oem 3 -c tessedit_char_whitelist=АБВГДЕЖЗИКЛМНОПРСТУФХЧШЩЭЮЯ0123456789',
        lang='rus',
    )
    return recognized_number