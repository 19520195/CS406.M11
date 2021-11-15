from config import *
import torch
import torch.backends.cudnn as cudnn

class modelYOLO:
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path = CFG_PATH_YOLO_MODEL)
        self.model.classes = [0] #Class: LP 
        self.model.conf = CFG_THRESHOLD
        if torch.cuda.is_available():
            cudnn.benchmark = True
        print("Loaded: YOLOv5")
            
    def predict(self, image):
        list_coors = [[int(box['xmin']), int(box['ymin']), int(box['xmax']), int(box['ymax'])] \
                for _, box in (self.model(image).pandas().xyxy.pop()).iterrows()]
        return list_coors