import cv2 
  
camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FPS, 30)
camera.set(3, 640)
camera.set(4, 480)

camera.set(cv2.CAP_PROP_FOURCC ,cv2.VideoWriter_fourcc('M','J','P','G'))
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y','1','6',' '))
# camera.set(cv2.CAP_PROP_CONVERT_RGB, 0)
  

while True: 
    ret, frame = camera.read() 
    cv2.imshow('frame', frame) 
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        break
  
camera.release() 
cv2.destroyAllWindows() 