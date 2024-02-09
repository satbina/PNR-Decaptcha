import os
import cv2
import numpy as np
from tqdm import tqdm
import pickle
path = 'train'
imageList = os.listdir(path)
imageList.remove("labels.txt")
with open("train/labels.txt", 'r') as file:
  Labels = file.readlines()
Labels = [line.rstrip('\n') for line in Labels]

Xtrain = []
ytrain = []

Xtest = []
ytest = []

trainRatio = 1

count = len(imageList)*trainRatio
i = 0 
for imageFile in imageList:
  if(i<count):
    #  add to train list
    Xtrain.append(imageFile)
    labelIndex = int(imageFile.split(".")[0])
    ytrain.append(Labels[labelIndex])
  else:
    Xtest.append(imageFile)
    labelIndex = int(imageFile.split(".")[0])
    ytest.append(Labels[labelIndex])
  i += 1
numTolabel = {0 : 'ODD',1: 'EVEN',}
labelTonum = {'ODD' : 0,'EVEN' : 1,}
def ImgProcessing_Seg():
  for imageIndex in tqdm(range(len(Xtrain))):
    img=cv2.imread(os.path.join(path, Xtrain[imageIndex]))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
    img[img==img[0,0]]=255
    kernel = np.ones((5,5), np.uint8) 
    img_d1 = cv2.dilate(img, kernel, iterations=1)
    img=cv2.cvtColor(img_d1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img,(3,3),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img = cv2.bitwise_not(th3)
    flag=0
    flag2=0
    start=0
    end=0
    for i in range(499,250,-1):
        for j in range(100):
            if(img[j,i]!=0):
                flag=1
                if(start==0):
                    start=i+5
                flag2=1    
        if(flag==0 and flag2==1):
            end=i-5
            if(start-end<60):
                continue
            else:
                break
        flag=0
    finalImage = img[:,end:start]
    finalImage = cv2.resize(finalImage, (50, 50))
    finalImage = finalImage.flatten()
    dfX.append(finalImage)
    dfy.append(labelTonum[ytrain[imageIndex]])
  return "success"

dfX = []
dfy = []
print(ImgProcessing_Seg())
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0,max_iter=4000)
classifier.fit(dfX,dfy)
svm_predictions = classifier.predict(dfX)
count = 0
for i in range(len(svm_predictions)):
    if svm_predictions[i] == dfy[i]:
        count += 1
print("ACCURACY OF THE MODEL: ", count/(i+1)*100)
filename = 'model.sav'
pickle.dump(classifier, open(filename, 'wb'))

