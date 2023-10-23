import cv2

import defines as dfns

class Yolo_OD:
    '''Класс нейросети'''

    def __init__(self, nn_info):
        '''Инициализация'''
        
        cfg_path = nn_info[0]
        weights_path = nn_info[1]
        nn_name = nn_info[2]

        print("--------------------------------------------")
        print("NN: Running OpenCV DNN with:", nn_name)

        self.nmsThreshold = 0.4
        self.confThreshold = 0.5
        self.image_size = 416

        # Загрузка нейросетки
        net = cv2.dnn.readNet(weights_path, cfg_path)

        # Включение CUDA, если умеется
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            print('NN: Enabled CUDA devices:',cv2.cuda.getCudaEnabledDeviceCount())
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16) # CUDA FP16
            # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA) # CUDA FP32
        else:
            print("NN: No CUDA devices")
            
        self.model = cv2.dnn_DetectionModel(net)
        
        # Загрузка классов
        self.classes = []
        self.load_class_names(dfns.NN_CLASSES)
        self.model.setInputParams(size=(self.image_size, self.image_size), scale=1/255)


    def load_class_names(self, classes_path):
        '''Загрузка классов'''

        with open(classes_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        print("NN: Load classes")


    def detect(self, frame):
        '''Детекция'''

        return self.model.detect(frame, 
                                nmsThreshold=self.nmsThreshold, 
                                confThreshold=self.confThreshold)


def draw_targets(frame, class_ids, scores, boxes, all_classes, find_label):
    '''Отрисовываем найденны цели'''

    FONT = cv2.FONT_HERSHEY_DUPLEX

    # Отрисовываем лейблы
    for i in range(len(boxes)):

        label = str(all_classes[int(class_ids[i])])

        if label == find_label:

            (x, y, w, h) = boxes[i]
            #print(int(class_ids[i]))
            label = str(all_classes[int(class_ids[i])])
            cx = int((x + x + w) / 2)
            cy = int((y + y + h) / 2)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(frame, label + ' ' + str(round(float(scores[i]),2)), \
                            (x,y - 10), FONT, 1.5, (0,0,255), 2)
    
    return frame


def NN_test():
    '''Тест работы нейросети'''

    # Кого ищем
    FIND_LABEL = "person"

    # Настройки камеры
    ADDRESS = 0
    CAM_RES = (640, 480)
    FPS = 30
    
    # Настройки нейросети
    CURENT_NN = dfns.NN_PATHS[2] # 0 - YOLO_V3_TINY, 1 - YOLO_V3, 2 - YOLO_V4_TINY, 3 - YOLO_V4

    # Камера
    camera = cv2.VideoCapture(ADDRESS)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,  CAM_RES[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_RES[1])
    camera.set(cv2.CAP_PROP_FPS, FPS)

    # Нейросеть
    od = Yolo_OD(CURENT_NN)
    with open(dfns.NN_CLASSES, "r") as f:
        all_classes = [line.strip() for line in f.readlines()]
    
    while True:

        ret, frame = camera.read()
        if not ret: 
            break

        (class_ids, scores, boxes) = od.detect(frame)
        frame = draw_targets(frame, class_ids, scores, boxes, all_classes, FIND_LABEL)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(10)
        if key == ord("q"): 
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    NN_test()