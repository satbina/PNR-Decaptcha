import os
import cv2
import numpy as np
from tqdm import tqdm
import pickle

# np.set_option('display.max_rows', 500)
path = "test"
imageList = os.listdir(path)
imageList.remove("lable.txt")
with open("train/lable.txt", "r") as file:
    Labels = file.readlines()
Labels = [line.rstrip("\n") for line in Labels]
i = 0
for lbl in Labels:
    for l in lbl:
        if (
            l != "1"
            and l != "2"
            and l != "3"
            and l != "4"
            and l != "5"
            and l != "6"
            and l != "7"
            and l != "8"
            and l != "9"
            and l != "0"
            and l != "+"
            and l != "-"
            and l != "="
            and l != "?"
        ):
            print(lbl)
            print(i)
    i += 1
Xtrain = []
ytrain = []

Xtest = []
ytest = []

trainRatio = 1

count = len(imageList) * trainRatio
i = 0
for imageFile in imageList:
    if i < count:
        #  add to train list
        Xtrain.append(imageFile)
        labelIndex = int(imageFile.split(".")[0])
        ytrain.append(Labels[labelIndex])
    else:
        Xtest.append(imageFile)
        labelIndex = int(imageFile.split(".")[0])
        ytest.append(Labels[labelIndex])
    i += 1
# print(Xtrain[65])
# print(ytrain[65])
numTolabel = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "+",
    11: "-",
    12: "=",
    13: "?",
}
labelTonum = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "+": 10,
    "-": 11,
    "=": 12,
    "?": 13,
}


def segment(image, st):
    flag = 0
    flag2 = 0
    start = 0
    end = 0
    for i in range(st, 149):
        for j in range(30):
            if image[j, i] != 0:
                flag = 1
                if start == 0:
                    start = i - 2
                flag2 = 1
        if flag == 0 and flag2 == 1:
            end = i + 2
            break
        flag = 0
    finalImage = image[:, start:end]
    return finalImage, end


def ImgProcessing_Seg():
    for imageIndex in tqdm(range(len(Xtrain))):
        # image=cv2.imread(os.path.join(path, Xtrain[imageIndex]))
        image = cv2.imread(os.path.join(path, Xtrain[imageIndex]), cv2.IMREAD_UNCHANGED)
        trans_mask = image[:, :, 3] == 0
        image[trans_mask] = [255, 255, 255, 255]
        image = cv2.bitwise_not(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        image = cv2.resize(image, (150, 30))
        end = 0
        # print(image)
        for i in range(len(ytrain[imageIndex])):
            finalImage, end = segment(image, end)
            finalImage = cv2.resize(finalImage, (25, 25))
            # print(finalImage.shape)
            # cv2.imshow("Image1"+str(i), finalImage)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            finalImage = finalImage.flatten()
            dfX.append(finalImage)
            # print(labelTonum[ytrain[imageIndex][i]])
            dfy.append(labelTonum[ytrain[imageIndex][i]])
    return "success"


dfX = []
dfy = []
print(ImgProcessing_Seg())
from sklearn.linear_model import LogisticRegression

classifier = LogisticRegression(random_state=0, max_iter=4000)
classifier.fit(dfX, dfy)
svm_predictions = classifier.predict(dfX)
count = 0
for i in range(len(svm_predictions)):
    if svm_predictions[i] == dfy[i]:
        count += 1
print("ACCURACY OF THE MODEL: ", count / (i + 1) * 100)
filename = "model.sav"
pickle.dump(classifier, open(filename, "wb"))
