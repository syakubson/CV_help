import cv2

from Camera_class import Camera

def MultiCamTest():
    '''Работа с несколькими камерами одновременно'''

    camera1 = Camera(0, (640,480), 30, True)
    camera2 = Camera(1, (640,480), 30, True)

    while True:
        
        ret1, frame1 = camera1.read_frame()  
        ret2, frame2 = camera2.read_frame()  
        
        cv2.imshow("Frame 1", frame1)
        cv2.imshow("Frame 2", frame2)

        if cv2.waitKey(10) == ord("q"):
            break 
    
    camera1.exit()
    camera2.exit()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    MultiCamTest()