import os
import cv2
import base64
import hashlib
import numpy as np
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, send_file, url_for, render_template

from config import *
from censorLicensePalate import *

# Load model
model = None
if CFG_MODEL == 'yolo':
    from modelYOLO import *
    model = modelYOLO()
else:
    from modelFasterRCNN import *
    model = modelFasterRCNN()
    
app = Flask(__name__)

# Check type HTTP
if CFG_HTTP_TYPE == 'ngrok':
    from flask_ngrok import run_with_ngrok
    run_with_ngrok(app)

# Hash file name
def getFileName():
    return hashlib.md5((str(datetime.now().time()) + "_CS406.M11").encode()).hexdigest() + ".jpg"

# Hash Image
def convertImageToBase64(image):
    return 'data:image/jpg;base64,' + base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()

@app.route('/')
def default():
    return '{"messages": "error"}'

@app.route('/', methods=['POST'])
def home():
    if request.method == 'GET':
        return '{"messages": "error"}'
    fileName = getFileName()
    imageByte = request.files['image'].read()     
    imageReplaceByte = request.files['imageReplace'].read()
    typeBlur = int(request.form['typeBlur'])
    kernelSize = int(request.form['kernelSize'])
    kernelDepth = int(request.form['kernelDepth'])
    
    if imageByte is None:
        return '{"messages": "error"}'
        
    imageArr = np.frombuffer(imageByte, dtype=np.uint8)
    image = cv2.imdecode(imageArr, flags=1)
    # cv2.imwrite(os.path.join(CFG_PATH_UPLOAD, fileName), image)
    listCoors = model.predict(image)
    imageResult = None
   
    
    if typeBlur == 5: # Replace image
        if imageReplaceByte is None:
            return '{"messages": "error"}'
        imageReplaceArr = np.frombuffer(imageReplaceByte, dtype=np.uint8)
        imageReplace = cv2.imdecode(imageReplaceArr, flags=1)
        imageResult = convertImage(image, listCoors).replaceImage(imageReplace)
    elif typeBlur == 1: # averageBlur
        imageResult = convertImage(image, listCoors).averageBlur(kernelSize)
    elif typeBlur == 2: # gaussianBlur
        imageResult = convertImage(image, listCoors).gaussianBlur(kernelSize)
    elif typeBlur == 3: # medianBlur
        imageResult = convertImage(image, listCoors).medianBlur(kernelSize)            
    elif typeBlur == 4: # eightBitsBlur
        kernelDepth = int(request.form['kernelDepth'])
        imageResult = convertImage(image, listCoors).eightBitsBlur(kernelSize, kernelDepth)
    
    # cv2.imwrite(os.path.join(CFG_PATH_RESULT, fileName), imageResult)

    return '{"messages": "success", "imageSrc": "' + convertImageToBase64(image) + '", "imageDes": "' + convertImageToBase64(imageResult) + '"}'
    
    # return '{"messages": "success", "imageSrc": "' + request.url[:-1] + url_for('displayImageSrc', filename=fileName) + '", "imageDes": "' + request.url[:-1] + url_for('displayImageDes', filename=fileName) + '"}'


# Rule Show Image Src
@app.route('/showSrc/<filename>')
def displayImageSrc(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
# Rule Show Image Des 
@app.route('/showDes/<filename>')
def displayImageDes(filename):
	return redirect(url_for('static', filename='results/' + filename), code=301)
    
if __name__ == '__main__':
    app.run()