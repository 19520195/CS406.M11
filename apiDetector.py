import cv2
import numpy as np
from flask import Flask, request

from config import *

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

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')

def home(path):
    if request.method == 'GET':
        return '{"messages": "error", "data": []}'
    imageByte = request.files['image'].read()
    if imageByte is None:
        return '{"messages": "error", "data": []}'
    imageArr = np.frombuffer(imageByte, dtype=np.uint8)
    image = cv2.imdecode(imageArr, flags=1)
    result = {
        "messages": "success",
        "data": model.predict(image)
    }
    return str(result).replace("'", '"')

if __name__ == '__main__':
    app.run()