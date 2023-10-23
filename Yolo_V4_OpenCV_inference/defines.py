MAIN_PATH = "./Yolo_V4_OpenCV_inference/"

YOLO_V3_TINY_CFG = MAIN_PATH + "yolo_models/yolov3-tiny.cfg"
YOLO_V3_TINY_WEIGHTS = MAIN_PATH + "yolo_models/yolov3-tiny.weights"
YOLO_V3_CFG = MAIN_PATH + "yolo_models/yolov3.cfg"
YOLO_V3_WEIGHTS = MAIN_PATH + "yolo_models/yolov3.weights"

YOLO_V4_TINY_CFG = MAIN_PATH + "yolo_models/yolov4-tiny.cfg"
YOLO_V4_TINY_WEIGHTS = MAIN_PATH + "yolo_models/yolov4-tiny.weights"
YOLO_V4_CFG = MAIN_PATH + "yolo_models/yolov4.cfg"
YOLO_V4_WEIGHTS = MAIN_PATH + "yolo_models/yolov4.weights"

NN_PATHS = [[YOLO_V3_TINY_CFG, YOLO_V3_TINY_WEIGHTS, "YOLO_V3_TINY"],
            [YOLO_V3_CFG, YOLO_V3_WEIGHTS, "YOLO_V3"],
            [YOLO_V4_TINY_CFG, YOLO_V4_TINY_WEIGHTS, "YOLO_V4_TINY"],
            [YOLO_V4_CFG,YOLO_V4_WEIGHTS, "YOLO_V4"]]

NN_CLASSES = MAIN_PATH + "yolo_models/all_classes.txt"