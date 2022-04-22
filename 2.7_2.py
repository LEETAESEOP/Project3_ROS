#예제 2.7은 웹캡 캡쳐부분이라 뺐음. 2.8에서 cv2.VideoCapture(0)만 넣어주면됨
#예제2.8 ''비디오 입력과 화면표시 2: 안드로이드 스마트폰 p31

import cv2
import os
import numpy as np
os.system('cls')

#크롭 영역(라인 추적 영역)
frame_crop_x1 = 0
frame_crop_y1 = 200
frame_crop_x2 = 639
frame_crop_y2 = 479

minLineLength = 5
maxLineGap = 10

#droid cam
cap = cv2.VideoCapture(0)  #노트북은 0 데스크탑은 1

# frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
#                 int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

frame_size = (1000, 1000)

print('frame_size = ', frame_size)

while True:
    retval, frame = cap.read()
    # 카메라를 뒤집어 쓸지 그대로 쓸지 선택하는곳
    # frame = cv2.flip(frame,1)
    # frame = cv2.flip(frame,0)
    original = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cropped = gray[frame_crop_y1:frame_crop_y2,frame_crop_x1:frame_crop_x2]
    # blurred = cv2.GaussianBlur(cropped, (5, 5), 0)
    blurred = cropped
    edged = cv2.Canny(blurred, 85, 85)
    lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
    max_diff = 1000
    final_x = 0
    if ( lines is not None ):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(original,(x1+frame_crop_x1,y1+frame_crop_y1),(x2+frame_crop_x1,y2+frame_crop_y1),(0,255,0),2)
            mid_point = ( x1 + x2 ) / 2
            diff = abs((320/2) - mid_point)
            if ( max_diff > diff ) :
                max_diff = diff
                final_x = mid_point
    
    if ( int(final_x) != 0 ) :
        original = cv2.circle(original,(int(final_x),int((frame_crop_y1+frame_crop_y2)/2)),5,(0,0,255),-1)
        original = cv2.rectangle(original,(int(frame_crop_x1),int(frame_crop_y1)),(int(frame_crop_x2),int(frame_crop_y2)),(0,0,255),1)
    frame = original
    
    if not retval:
        break
    cv2.imshow('frame', frame)
    theta = int(( int(final_x) - 160.0 ) / 320.0 * 100)
    print(theta)
    key = cv2.waitKey(25)
    if key == 27: #ESC
        break

if cap.isOpened():
    cap.release()

cv2.destroyAllWindows()