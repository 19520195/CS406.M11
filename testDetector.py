import os
import cv2
import time
from modelYOLO import *
from modelFasterRCNN import *

def getResult(model, pathImage):
    image = cv2.imread(pathImage)
    startTime = time.time()
    result = model.predict(image)
    totalTime = time.time() - startTime
    return result, totalTime
    
def printResult(modelName, pathInput, result, time):
    print("Model: ", modelName)
    print("Input: ", pathInput)
    print("Result: ", result)
    print("Time: {:.2f}".format(time))
    print("----------------------------")
    
def saveResultDetector(pathSave, fileName, pathImage, listCoors):
    pathSaveFile = pathSave + fileName + ".jpg"
    image = cv2.imread(pathImage)
    for x1, y1, x2, y2 in listCoors:
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imwrite(pathSaveFile, image)
    print("Done:", pathSaveFile)

model_1 = modelYOLO()
model_2 = modelFasterRCNN()

pathImage_1 = 'testcases/input/image_1.jpg'
pathImage_2 = 'testcases/input/image_2.jpg'
pathSaveDetector = 'testcases/outputDetector/'


# get Time

print("[=========> Image_1")
res_1_1, time_1_1 = getResult(model_1, pathImage_1)
res_1_2, time_1_2 = getResult(model_2, pathImage_1)
printResult("YOLOv5", pathImage_1, res_1_1, time_1_1)
printResult("FasterRCNN", pathImage_1, res_1_2, time_1_2)

print("\n\n=================\n\n")

print("[=========> Image_2")
res_2_1, time_2_1 = getResult(model_1, pathImage_2)
res_2_2, time_2_2 = getResult(model_2, pathImage_2)
printResult("YOLOv5", pathImage_1, res_2_1, time_2_1)
printResult("FasterRCNN", pathImage_1, res_2_2, time_2_2)

# get Detector Result

saveResultDetector(pathSaveDetector, "YOLOv5_image_1", pathImage_1, res_1_1)
saveResultDetector(pathSaveDetector, "FasterRCNN_image_1", pathImage_1, res_1_2)

saveResultDetector(pathSaveDetector, "YOLOv5_image_2", pathImage_2, res_2_1)
saveResultDetector(pathSaveDetector, "FasterRCNN_image_2", pathImage_2, res_2_2)
