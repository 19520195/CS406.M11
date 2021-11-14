from config import *
from modelYOLO import *
from modelFasterRCNN import *
import cv2
import base64
import json
import numpy as np
from flask import Flask, request
from censorLicensePalateAPI import *

# detector = None
# if CFG_API_TYPE == 'fasterrcnn':
    # detector = modelFasterRCNN()
# else:
model = modelYOLO()
    
app = Flask(__name__)

# if CFG_API_DEVICE == 'colab':
    # from flask_ngrok import run_with_ngrok
    # run_with_ngrok(app)

def convertImageToBase64(image):
    return 'data:image/jpg;base64,' + base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')

def home(path):
    if request.method == 'GET':
        return '{"messages": "error"}'

    imageByte = request.files['image'].read()
    typeBlur = int(request.form['typeBlur'])
    imageReplaceByte = request.files['imageReplace'].read()
    kernelSize = int(request.form['kernelSize'])
    
    if imageByte is None:
        return '{"messages": "error"}'
        
    imageArr = np.frombuffer(imageByte, dtype=np.uint8)
    image = cv2.imdecode(imageArr, flags=1)
    
    list_coors = model.predict(image)
    imageResult = None
    
    if typeBlur == 6:
        if imageReplaceByte is None:
            return '{"messages": "error"}'
        imageReplaceArr = np.frombuffer(imageReplaceByte, dtype=np.uint8)
        imageReplace = cv2.imdecode(imageReplaceArr, flags=1)
        imageResult = convertImage(image, list_coors).replaceImage(imageReplace)
    elif typeBlur == 1:
        imageResult = convertImage(image, list_coors).averageBlur(kernelSize)
    elif typeBlur == 2:
        imageResult = convertImage(image, list_coors).GaussianBlur(kernelSize)
    elif typeBlur == 3:
        imageResult = convertImage(image, list_coors).medianBlur(kernelSize)            
    elif typeBlur == 4:
        #Nha
        imageResult = convertImage(image, list_coors).GaussianBlur(kernelSize)
    elif typeBlur == 5:
        #Nha
        imageResult = convertImage(image, list_coors).GaussianBlur(kernelSize)
    
    # f = open("a.html", "w", encoding="utf-8")
    # f.write('<img src="' + convertImageToBase64(imageResult) + '">')
    # f.close()
    return '{"messages": "success", "img_base64": "' + convertImageToBase64(image) + '", "img_res_base64": "' + convertImageToBase64(imageResult) + '"}'

if __name__ == '__main__':
    app.run()