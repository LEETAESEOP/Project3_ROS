#예제 2.7은 웹캡 캡쳐부분이라 뺐음. 2.8에서 cv2.VideoCapture(0)만 넣어주면됨
#예제2.8 ''비디오 입력과 화면표시 2: 안드로이드 스마트폰 p31

import cv2, pafy
import os
os.system('cls')

#droid cam
cap = cv2.VideoCapture(0)  #노트북은 0 데스크탑은 1

frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

print('frame_size = ', frame_size)

while True:
    retval, frame = cap.read()
    if not retval:
        break
    cv2.imshow('frame', frame)

    key = cv2.waitKey(25)
    if key == 27: #ESC
        break

if cap.isOpened():
    cap.release()

cv2.destroyAllWindows()