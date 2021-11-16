# THRESHOLD
CFG_THRESHOLD = 0.6

# YOLO
CFG_PATH_YOLO_MODEL = './model/YOLOV5.pt'

# FASTER RCNN
CFG_PATH_FASTERRCNN_CONFIG = './model/config_FasterRCNN.txt'
CFG_PATH_FASTERRCNN_MODEL = './model/faster-rcnn-data-raw.pth'

# DEVICE
CFG_DEVICE = 'cpu' # ['cpu' , 'gpu'] 

# MODEL
CFG_MODEL = 'yolo' # ['yolo' , 'fasterrcnn']

# HTTP SERVER
CFG_HTTP_TYPE = 'ngrok' # ['local' , 'ngrok']

# CUSTOM
CFG_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
CFG_PATH_UPLOAD = './static/uploads'
CFG_PATH_RESULT = './static/results'
CFG_MAX_CONTENT_LENGTH = 5 * 1024 * 1024 # 5MB
