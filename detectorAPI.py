from config import *
from modelYOLO import *
from modelFasterRCNN import *
import cv2
import json
import numpy as np
from flask import Flask, request

detector = None
if CFG_API_TYPE == 'fasterrcnn':
    detector = modelFasterRCNN()
else:
    detector = modelYOLO()
    
app = Flask(__name__)

if CFG_API_DEVICE == 'colab':
    from flask_ngrok import run_with_ngrok
    run_with_ngrok(app)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')

def home(path):
    if request.method == 'GET':
        return '{"messages": "error", "data": []}'
        
    image_byte = request.files['image'].read()
    if image_byte is None:
        return '{"messages": "error", "data": []}'
        
    image_arr = np.frombuffer(image_byte, dtype=np.uint8)
    image = cv2.imdecode(image_arr, flags=1)
    
    result = {
        "messages": "success",
        "data": detector.predict(image)
    }
    return str(result).replace("'", '"')

if __name__ == '__main__':
    app.run()