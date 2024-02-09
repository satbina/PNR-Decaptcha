# DO NOT CHANGE THE NAME OF THIS METHOD OR ITS INPUT OUTPUT BEHAVIOR

# INPUT CONVENTION
# filenames: a list of strings containing filenames of images

# OUTPUT CONVENTION
# The method must return a list of strings. Make sure each string is either "ODD"
# or "EVEN" (without the quotes) depending on whether the hexadecimal number in
# the image is odd or even. Take care not to make spelling or case mistakes. Make
# sure that the length of the list returned as output is the same as the number of
# filenames that were given as input. The judge may give unexpected results if this
# convention is not followed.
import cv2
import numpy as np
import pickle


def decaptcha(filenames):
    # Invoke your model here to make predictions on the images
    loaded_model = pickle.load(open("model.sav", "rb"))
    numTolabel = {
        0: "ODD",
        1: "EVEN",
    }
    X = []
    for i in filenames:
        img = cv2.imread(i)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img[img == img[0, 0]] = 255
        img_d1 = cv2.dilate(img, np.ones((5, 5), np.uint8), iterations=1)
        img = cv2.cvtColor(img_d1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(img, (3, 3), 0)
        ret3, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img = cv2.bitwise_not(th)
        flag = 0
        flag2 = 0
        start = 0
        end = 0
        for i in range(499, 250, -1):
            for j in range(100):
                if img[j, i] != 0:
                    flag = 1
                    if start == 0:
                        start = i + 5
                    flag2 = 1
            if flag == 0 and flag2 == 1:
                end = i - 5
                if start - end < 60:
                    continue
                else:
                    break
            flag = 0
        img = img[:, end:start]
        img = cv2.resize(img, (50, 50))
        img = img.flatten()
        X.append(img)
        y_pred = loaded_model.predict(X)
    labels = []
    for i in y_pred:
        labels.append(numTolabel[i])
    return labels
