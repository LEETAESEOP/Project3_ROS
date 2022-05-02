<<<<<<< HEAD
#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyzbar.pyzbar as pyzbar
import rospy
from geometry_msgs.msg import Twist
import cv2
import numpy as np
import math
import time
# import serial

## 변수 쌓아두는곳
frame_crop_x1 = 0
frame_crop_y1 = 120
=======
#예제 2.7은 웹캡 캡쳐부분이라 뺐음. 2.8에서 cv2.VideoCapture(0)만 넣어주면됨
#예제2.8 ''비디오 입력과 화면표시 2: 안드로이드 스마트폰 p31
# ddepth 가 뭔가?

import cv2
import os
import numpy as np
import time
os.system('cls')

# 이미지 사이즈 320x240
# #크롭 영역(라인 추적 영역)
# image_crop_x1 = 0
# image_crop_y1 = 100
# image_crop_x2 = 319
# image_crop_y2 = 239

# 이미지 사이즈 640 * 480
#크롭 영역(라인 추적 영역)
frame_crop_x1 = 0
frame_crop_y1 = 200
>>>>>>> e56088acd7395d11cc447369aa4903a2f9b1d7af
frame_crop_x2 = 639
frame_crop_y2 = 479

minLineLength = 40
maxLineGap = 20

<<<<<<< HEAD
##아두이노 변수 값###
# ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
# distances = ""
# myData = 0
# distance_num = 0

## 이동체 이동 속도 및 회전 각도
speed = 0
Angle = 0
avr_x = 0
rccar_stop = 0


## qr코드 종류
code_start = "start"
code_0 = "A"
code_1 = "B"
code_2 = "C"
barcode_data_line_QR = []
text_0 = ""
text_1 = ""

cap_0 = cv2.VideoCapture(0)     ## cap_0 은 바닥보면서 레일과 큐알확인
cap_1 = cv2.VideoCapture(2)     ## cap_1 은 사물적재 위치를 보면서 큐알확인

def talker():
    global Angle, speed, barcode_data_line_QR, text_0, text_1, avr_x, rccar_stop, myData, distance_num
    rospy.init_node("line_qr_sensor")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=100)
    
    msg = Twist()
    # loop_rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        ############################## 공통 파트  ##############################

        # 메시지 발신
        msg.linear.x = speed
        msg.angular.z = Angle
        pub.publish(msg)

        if rccar_stop == 1 :
            time.sleep(1)
            rccar_stop = 0

        retval_0, frame_0 = cap_0.read()
        retval_1, frame_1 = cap_1.read()
        original = frame_0
        gray_line_0 = cv2.cvtColor(frame_0, cv2.COLOR_BGR2GRAY)
        gray_line_1 = cv2.cvtColor(frame_0, cv2.COLOR_BGR2GRAY)
        gray_product_0 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)


        # 시간간격을 계산해서 해당 시간이 벗어났을때 처리를 유지 그 안에 들어오는 처리는 무시


        # 관문을 지킴. 특정 플래그에 따라서 여기서 반복문을 돌려보낼지 이어갈지





        ############################## 레일 인식 파트 (line_0)  ##############################
        blurred = gray_line_0[frame_crop_y1:frame_crop_y2,frame_crop_x1:frame_crop_x2]
        blurred = cv2.boxFilter(blurred, ddepth=-1, ksize=(31,31))
        retval2 ,blurred = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
        edged = cv2.Canny(blurred, 85, 85)
        lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
        max_diff = 1000
        final_x = 0
        if ( lines is not None ):
            if ( lines is not None ):
                add_line = 0
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(original,(x1+frame_crop_x1,y1+frame_crop_y1),(x2+frame_crop_x1,y2+frame_crop_y1),(0,255,0),3)
                    mid_point = ( x1 + x2 ) / 2
                    # 화면 중앙 x값과, 녹색선의 중앙x값의 차이값을 구한다.
                    diff = abs((640/2) - mid_point)
                    # print("mid_point, diff", mid_point, diff)
                    if ( max_diff > diff ) :
                        max_diff = diff
                        # final_x : 녹색선 중앙의 x 좌표점이 된다.
                        final_x = mid_point
                    add_line = add_line + final_x
                avr_x = add_line / len(lines)


            if ( int(avr_x) != 0 ) :
                original = cv2.circle(original,(int(avr_x),int((frame_crop_y1+frame_crop_y2)/2)),5,(0,0,255),-1)
                original = cv2.rectangle(original,(int(frame_crop_x1),int(frame_crop_y1)),(int(frame_crop_x2),int(frame_crop_y2)),(0,0,255),1)
            frame_0 = original
            
            if not retval_0:
                break
            theta = int(( int(avr_x) - 320.0 ) / 640.0 * 100)
        if ( lines is None ):
            theta = -50

        ############################## QR 인식 파트 (line_1)  ##############################

        decoded_line_QR = pyzbar.decode(gray_line_1)

        for _ in decoded_line_QR:                                                                                               # decoded 정보를 변수 d에 넣음 으로써 루프를 돌림. 
            x, y, w, h = _.rect                                                                                 # QR을 인식할때 시각적으로 QR코드의 사각형을 만듬
            barcode_data_line_QR = _.data.decode("utf-8")                                                               # QR 안에 들어있는 정보들을 저장시켜놓음
            barcode_type_line_QR = _.type                                                                               # 인식하고 있는것이 QR인지 barcode인지 알 수 있음.
            cv2.rectangle(frame_0, (x, y), (x + w, y + h), (0, 0, 255), 2)                                      # OpenCv를 통해서 QR코드를 인식할 때, 사각형을 시각적으로 보여주고 색상까지 정할 수 있음
            text_0 = '%s (%s)' % (barcode_data_line_QR, barcode_type_line_QR)                                                     # QR코드 안에 어떤 정보인지, 어느 타입인지 문구를 통해 알 수 있게 함
            cv2.putText(frame_0, text_0, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)      # openCv를 통해 QR코드 안에 정보와 타입을 시각적으로 표현할 수 있게 한다.

        if decoded_line_QR == [] :
            barcode_data_line_QR = "QR_X"

        ############################## QR 인식 파트 (product_0)  ##############################

        decoded_product_QR = pyzbar.decode(gray_product_0)

        for _ in decoded_product_QR:                                                                                               # decoded 정보를 변수 d에 넣음 으로써 루프를 돌림. 
            a, b, c, d = _.rect                                                                                 # QR을 인식할때 시각적으로 QR코드의 사각형을 만듬
            barcode_data_product_QR = _.data.decode("utf-8")                                                               # QR 안에 들어있는 정보들을 저장시켜놓음
            barcode_type_product_QR = _.type                                                                               # 인식하고 있는것이 QR인지 barcode인지 알 수 있음.
            cv2.rectangle(frame_1, (a, b), (a + c, b + d), (0, 0, 255), 2)                                      # OpenCv를 통해서 QR코드를 인식할 때, 사각형을 시각적으로 보여주고 색상까지 정할 수 있음
            text_1 = '%s (%s)' % (barcode_data_product_QR, barcode_type_product_QR)                                                     # QR코드 안에 어떤 정보인지, 어느 타입인지 문구를 통해 알 수 있게 함
            cv2.putText(frame_1, text_1, (a, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)      # openCv를 통해 QR코드 안에 정보와 타입을 시각적으로 표현할 수 있게 한다.

        if decoded_product_QR == [] :
            barcode_data_product_QR = "QR_X"

        ############################## 터미널 출력 창 ##############################
        # print('theta : %d' % theta )
        # print("line_QR : %s" % barcode_data_line_QR)
        # print("product_QR : %s" % barcode_data_product_QR)

        cv2.imshow('frame_0', frame_0)
        cv2.imshow('frame_1', frame_1)

        ############################## 이동 속도 제어 및 회전 관리 조건 ##############################
        Angle = (-theta *1.8) * (np.pi / 180) / 3 * 2 ## Angle == 1.57 -> 90'
        speed = 0.4 - abs(Angle * 0.2)
        # print('Angle : %f' % Angle)
        
        # if int(distance_num) >= 30:
        if barcode_data_product_QR != "QR_X" :                      ## QR코드에 올라온 물건이 있을때
            if barcode_data_product_QR != barcode_data_line_QR :    ## QR코드에 올라온 물건과 QR라인이 동일하지 않을때
                # if theta != -50:
                #     if theta <  -40                :                        speed = 0.2
                #     if theta >= -40 and theta < -30:                        speed = 0.2
                #     if theta >= -30 and theta < -20:                        speed = 0.2
                #     if theta >= -20 and theta < -10:                        speed = 0.3
                #     if theta >= -10 and theta <  10:
                #         speed = 0.35
                #         Angle = 0
                #     if theta >=  10 and theta <  20:                        speed = 0.3
                #     if theta >=  20 and theta <  30:                        speed = 0.2
                #     if theta >=  30 and theta <  40:                        speed = 0.2
                #     if theta >=  40                :                        speed = 0.2
                if theta == -50:
                    speed = 0
                    Angle = -0.3
            if barcode_data_product_QR == barcode_data_line_QR :
                speed = 0       
                Angle = 0                               
                rccar_stop = 1

        if barcode_data_product_QR == "QR_X" :                                                     ## QR코드에 올라온 물건이 없을때
            if barcode_data_line_QR != "start":                     ## QR라인이 START가 아닐때
                # if theta != -50:
                #     if theta <  -40                :                        speed = 0.2
                #     if theta >= -40 and theta < -30:                        speed = 0.2
                #     if theta >= -30 and theta < -20:                        speed = 0.2
                #     if theta >= -20 and theta < -10:                        speed = 0.3
                #     if theta >= -10 and theta <  10:
                #         speed = 0.35
                #         Angle = 0
                #     if theta >=  10 and theta <  20:                        speed = 0.3
                #     if theta >=  20 and theta <  30:                        speed = 0.2
                #     if theta >=  30 and theta <  40:                        speed = 0.2
                #     if theta >=  40                :                        speed = 0.2
                if theta == -50:
                    speed = 0
                    Angle = -0.3
            if barcode_data_line_QR == "start" :
                speed = 0                                        
                Angle = 0
                rccar_stop = 1
        # if int(distance_num) < 30:
        #     speed = 0                                        
        #     Angle = 0
        #     rccar_stop = 1

        key = cv2.waitKey(25)
        if key == 27: #ESC
            break

        # print(Angle, speed)
        # if (ser.inWaiting()>0):
        #     myData = ser.readline().decode()
        # print(myData[:len(myData)-1])    
        # distance_num = myData[:len(myData)-1]
        # print(distance_num)
    

if __name__ == "__main__":
    try:
        talker()
    except rospy.ROSInterruptException:
        pass




=======
#droid cam
cap = cv2.VideoCapture(0)  #노트북은 0 데스크탑은 1

# 원본 동영상 크기 정보
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("원본 동영상 너비(가로) : {}, 높이(세로) : {}".format(w, h))

# 동영상 크기 변환 원할시 아래 주석 풀고 숫자만 바꿔주면 된다.
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) # 가로
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # 세로


while True:
    retval, frame = cap.read()
    # 카메라를 뒤집어 쓸지 그대로 쓸지 선택하는곳
    # frame = cv2.flip(frame,1)
    # frame = cv2.flip(frame,0)
    # frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY)
    original = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(cropped, (5, 5), 0)
    blurred = gray[frame_crop_y1:frame_crop_y2,frame_crop_x1:frame_crop_x2]

    # 아래 두줄 추가한 부분
    # 영상을 부드럽게 하는 블러필터 중 boxFilter를 사용하여 영상의 잡음을 제거하고 영상을 부드럽게 한다.
    # ddepth = -1 이면 blurred 와 같은 깊이다. ksize가 클수록 화면이 더 부드러워진다.  
    blurred = cv2.boxFilter(blurred, ddepth=-1, ksize=(31,31))
    # cv2.threshold(img, threshold_value, value, flag) 형식이다.
    # threshold는 임계값 영상을 출력한다. THRESH_BINARY를 사용하면 2개의 값만 갖는다.(흑,백)
    # 아래에서 100=임계점이며, 0~100 의 값들은 255로 표현된다. 255=완전 백색을 의미한다.
    retval2 ,blurred = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
    cv2.imshow('blurred', blurred)

    
    
    # cv2.Canny(gray_img, threshold1, threshold2) 형식이다.
    # cv2.Canny() 는 엣지 검출 함수다. 이미지의 엣지만을 리턴한다.
    # threshold1 = 낮은 경계값(0~255), threshold2 = 높은 경계값(0~255)
    # threshold1, threshold2 값의 숫자가 클수록 엣지가 검출되기 어렵다.
    edged = cv2.Canny(blurred, 85, 85)
    cv2.imshow('edged', edged)
    # 허프(Hough) 변환. 이미지의 Line을 찾는것이 목적이다.
    # HoughLinesP 설명     (img, rho, theta, threshold, lines, minLineLength, maxLineGap)
    # img : 8bit, single-channel binary image, canny edge를 선 적용.
    # rho : r 값의 범위 (0 ~ 1 실수),        theta: 각도, 라디안 단위 (np.pi/0~180)
    # threshold: 직선으로 판단할 최소한의 동일 개수(점의 개수) (작은 값: 정확도 감소, 검출 개수 증가 / 큰 값: 정확도 증가, 검출 개수 감소)
    # minLineLength : 선으로 인정할 최소 길이. 이 값보다 작으면 reject.
    # maxLineGap = 직선 위의 에지들의 최대 허용간격. 이 값보다 작으면 reject. (에지가 중간에 끊겼을때 1로하면 조금만 끊겨도 선을 끊어버림.)
    lines = cv2.HoughLinesP(edged, 1, np.pi/180, 10, minLineLength, maxLineGap)
    #lines : 10개일경우 아래처럼 데이타 출력된다.
    #     S좌표    F좌표
    #  [ x1   y1 / x2  y2 ]
    # [[[151 182 165 160]]
    # [[467 104 471 114]]      
    # [[136 205 146 189]]      
    # [[203 100 224  64]]      
    # [[514 231 519 246]]      
    # [[454  74 458  84]]
    # [[501 192 504 202]]
    # [[166 159 176 143]]
    # [[ 99 264 118 235]]
    # [[484 145 489 159]]]


    max_diff = 1000
    final_x = 0

    # 라인이 검출될 때
    if ( lines is not None ):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # print("x1, y1, x2, y2", line[0])
            # 녹색 선 그리기
            # 이미지 파일, 시작점 좌표, 종료점 좌표, 선색상, 선두께) 
            cv2.line(original,(x1+frame_crop_x1,y1+frame_crop_y1),(x2+frame_crop_x1,y2+frame_crop_y1),(0,255,0),3)
            # 녹색선의 x위치 중간값
            mid_point = ( x1 + x2 ) / 2
            # 화면 중앙 x값과, 녹색선의 중앙x값의 차이값을 구한다.
            diff = abs((640/2) - mid_point)
            # print("mid_point, diff", mid_point, diff)
            if ( max_diff > diff ) :
                max_diff = diff
                # final_x : 녹색선 중앙의 x 좌표점이 된다.
                final_x = mid_point
    
    if ( int(final_x) != 0 ) :
        # 빨간점 인식 포인트, 이때 녹색선의 x값 중앙점을 가르킴. y좌표는 화면 중앙. 원 두께는 5
        original = cv2.circle(original,(int(final_x),int((frame_crop_y1+frame_crop_y2)/2)),5,(0,0,255),-1)
        # 빨간 사각 영역
        original = cv2.rectangle(original,(int(frame_crop_x1),int(frame_crop_y1)),(int(frame_crop_x2),int(frame_crop_y2)),(0,0,255),1)
    frame = original
    
    # 카메라 입력값 없으면 break
    if not retval:
        break
    # 최종 화면
    cv2.imshow('frame', frame)
    theta = int(( int(final_x) - 320.0 ) / 640.0 * 100)
    print("theta: ", theta)
    
    key = cv2.waitKey(25)
     # ESC 입력시 종료
    if key == 27: #ESC 아스키코드값이 27
        break

if cap.isOpened():
    cap.release()

cv2.destroyAllWindows()
>>>>>>> e56088acd7395d11cc447369aa4903a2f9b1d7af
