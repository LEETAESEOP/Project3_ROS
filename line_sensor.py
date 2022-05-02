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
frame_crop_x2 = 639
frame_crop_y2 = 479

minLineLength = 40
maxLineGap = 20

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




