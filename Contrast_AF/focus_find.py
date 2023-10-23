import numpy as np
import cv2

def find_SF(image, focus_zone, matrix_type="sobel"):
    '''Поиск значения фокуса. Изображение, координаты зоны фокуса, тип используемой матрицы sobel/laplas'''

    if matrix_type == "sobel":
        # Сумма вертикальной и горизонтальной матриц Собеля
        matrix = np.array([[2,  2,  0],
                           [2,  0, -2],
                           [0, -2, -2]])
    
    elif matrix_type == "laplas":
        # Матрица Лапласа
        matrix = np.array([[-1, -1, -1],   
                           [-1,  8, -1],
                           [-1, -1, -1]])

    # Перевод в ЧБ, если пришло цветное изображение
    if image.shape == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Вырезаем область для поиска фокуса
    x1, y1, x2, y2 = focus_zone
    focus_zone = image[y1:y2, x1:x2]

    # Поиск фокуса
    focus_zone = cv2.filter2D(focus_zone, -1, matrix)   # Свёртка с матрицей
    sr_kv_grad = np.sum(focus_zone)                     # Срений квадрат градиента
    focus_size_sqr = int(abs(x2 - x1))*(abs(y2 - y1))   # Квадрат размера зоны фокуса    
    sf = sr_kv_grad/focus_size_sqr                      # Значение фокуса

    return sf


def sf_filter(sf, sf_prev):
    '''Фильтрация значений фокуса'''

    return sf_prev * 0.8 + sf * 0.2


def af_test():
    '''Тест поиска фокуса'''

    # Настройки камеры
    ADDRESS = 0
    CAM_RES = (640, 480)
    FPS = 30

    # Камера
    camera = cv2.VideoCapture(ADDRESS)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,  CAM_RES[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_RES[1])
    camera.set(cv2.CAP_PROP_FPS, FPS)
    
    # Настройка положения зоны поиска фокуса (по центу кадра)
    focus_size = 60 # Размер зоны поиска фокуса
    focus_zone = ((CAM_RES[0] - focus_size)//2,
                  (CAM_RES[1] - focus_size)//2,
                  (CAM_RES[0] + focus_size)//2,
                  (CAM_RES[1] + focus_size)//2
                 ) # Координаты зоны фокусировки
    sf = 0
    sf_prev = 0
    
    while True:

        ret, frame = camera.read()
        if not ret: break
        
        # Поиск значения фокуса и его фильтрация
        sf = find_SF(frame, focus_zone, "sobel")
        sf_fil = sf_filter(sf, sf_prev)
        sf_prev = sf_fil
        
        print(f'Focus value: {sf_fil}')

        # Отрисовка зоны фокуса
        cv2.rectangle(frame, focus_zone[2:], focus_zone[:2], (0, 0, 255), 2)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(10)
        if key == ord("q"): break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    af_test()