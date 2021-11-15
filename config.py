# THRESHOLD
CFG_THRESHOLD = 0.6

# YOLO
CFG_PATH_YOLO_MODEL = './model/best.pt'

# FASTER RCNN
CFG_PATH_FASTERRCNN_CONFIG = './model/config_FasterRCNN.txt'
CFG_PATH_FASTERRCNN_MODEL = './model/model_0004999.pth'

# DEVICE
CFG_DEVICE = 'cpu' # ['cpu' , 'gpu'] 

# MODEL
CFG_MODEL = 'yolo' # ['yolo' , 'fasterrcnn']

# HTTP SERVER
CFG_HTTP_TYPE = 'local' # ['local' , 'ngrok']