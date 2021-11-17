from config import *
import os
import sys
import detectron2
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

class modelFasterRCNN:
    def __init__(self):
        temp = sys.stderr
        sys.stderr = open(os.devnull, "w")
        cfg = get_cfg()
        cfg.merge_from_file(CFG_PATH_FASTERRCNN_CONFIG)
        cfg.MODEL.WEIGHTS = CFG_PATH_FASTERRCNN_MODEL
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = CFG_THRESHOLD
        cfg.MODEL.DEVICE = CFG_DEVICE
        cfg.freeze()
        self.predictor = DefaultPredictor(cfg)
        sys.stderr = temp
        print("Loaded: FASTER RCNN")
        
    def predict(self, image):
        if CFG_DEVICE != "cpu":
            return [[int(_) for _ in x] for x in self.predictor(image)["instances"].pred_boxes.tensor.cpu().numpy().tolist()] 
        return [[int(_) for _ in x] for x in self.predictor(image)["instances"].pred_boxes.tensor.numpy().tolist()] 