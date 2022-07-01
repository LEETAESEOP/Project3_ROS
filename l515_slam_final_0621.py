#!/usr/bin/python3
# -*- coding: utf-8 -*-

## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

from os import system
import realsense2_camera as realcamera
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
import pyrealsense2 as rs
import numpy as np
import rospy
import time
import os
import cv2
import pyzbar.pyzbar as pyzbar
from matplotlib import pyplot as plt
from io import BytesIO
import math

speed = 0
angle = 0

limit = 2000

count = 0
data_all = []
view_data_all = []
data_data_all = []
data_data_0 = []
data_data_0_np = []
data_data_1 = []
data_data_1_np = []
data_data_01 = []
data_data_all = []

obstacle_view = 0
## mapping = ["매핑준비중", "매핑진행중", "매핑종료", "매핑완료"]
mapping = "매핑준비중"
qr_moving = "QR대기중"
qr_target = "QR_X"
qr_moving_step = "QR대기중"
run_direction = "정면"

my_distance = 0
my_angle = 0


## QR_A = 거리 3m // 각도 30'
## QR_B = 거리 4m // 각도 50'
## QR_C = 거리 4m // 각도 100'

QR_A_distance = 2.9
QR_A_angle = 30
QR_B_distance = 3.5
QR_B_angle = 60
QR_C_distance = 3.5
QR_C_angle = 105

#############################################################################################################################################################################
#############################################################################################################################################################################
################################################################ !!!!!!!!!!!!!!! 캡 자주바뀜 !!!!!!!!!!!!!!! ################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################

cap_1 = cv2.VideoCapture(10)

cap_1.set(cv2.CAP_PROP_FRAME_HEIGHT,200)
cap_1.set(cv2.CAP_PROP_FRAME_WIDTH,320)


def lidar_pose(data):
    global position_x, position_y, orientation_x, orientation_y, orientation_z, orientation_w, roll_x, pitch_y, yaw_z
    try :
        orientation_x = round(data.pose.pose.orientation.x,1)
        orientation_y = round(data.pose.pose.orientation.y,1)
        orientation_z = round(data.pose.pose.orientation.z,1)
        orientation_w = round(data.pose.pose.orientation.w,1)
        
        position_x = round((data.pose.pose.position.x),1)
        position_y = round((data.pose.pose.position.y),1)
        
        # round_x = round(position_x,1)
        # round_y = round(position_y,1)
        # round_x = int(position_x)
        # round_y = int(position_y)
        
        t0 = +2.0 * (orientation_w * orientation_x + orientation_y * orientation_z)
        t1 = +1.0 - 2.0 * (orientation_x * orientation_x + orientation_y * orientation_y)
        roll_x = math.atan2(t0, t1)
        roll_x = round((roll_x * 180 / math.pi),3)

        t2 = +2.0 * (orientation_w * orientation_y - orientation_z * orientation_x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
        pitch_y = round((pitch_y * 180 / math.pi),3)

        t3 = +2.0 * (orientation_w * orientation_z + orientation_x * orientation_y)
        t4 = +1.0 - 2.0 * (orientation_y * orientation_y + orientation_z * orientation_z)
        yaw_z = math.atan2(t3, t4)
        yaw_z = round((yaw_z * 180 / math.pi),3)

        return roll_x, pitch_y, yaw_z
    except : pass

def cam_lidar_read(data):
    global count, data_data_0, data_data_1, angle, speed, mapping, qr_moving, qr_target, qr_moving_step, my_distance, my_angle, run_direction
    global barcode_data_product_QR, barcode_type_product_QR, decoded_product_QR, retval_1, frame_1, cap_1



    retval_1, frame_1 = cap_1.read()

    decoded_product_QR = pyzbar.decode(frame_1)
    for _ in decoded_product_QR:
        a, b, c, d = _.rect
        barcode_data_product_QR = _.data.decode("utf-8")
        barcode_type_product_QR = _.type
        cv2.rectangle(frame_1, (a, b), (a + c, b + d), (0, 0, 255), 2)
        text_1 = '%s (%s)' % (barcode_data_product_QR, barcode_type_product_QR)
        cv2.putText(frame_1, text_1, (a, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        
    if decoded_product_QR == [] :
        barcode_data_product_QR = "QR_X"
    
    # cv2.imshow('Video', frame_1)

    cv2.waitKey(1)



    
    try :
        view_data_all.clear()
        data_data_0.clear()
        data_data_1.clear()


        data_data = data.data
        data_data_arr = bytearray(data_data)

        # index 0부터 두칸 간격으로 
        data_data_0 = data_data_arr[0::2]
        data_data_0_np = np.array(data_data_0)

        data_data_1 = data_data_arr[1::2]
        data_data_1_np = np.array(data_data_1)
        data_data_1_np = data_data_1_np * 256

        data_data_01 = np.array([data_data_0_np,data_data_1_np])    
        data_data_all = data_data_01.sum(axis=0)
        

        xy = 0

        add_num = 0
        add_edge_num = 0
        add_edge_remain_num = 0
        
        os.system('clear') 

        print("--------------------------------")

        # for y in range(480) :
        for y in range(480) :
            # xy = 0 ~ 307200
            xy = y * 640

            # y = 0 ~ 12 
            if y % 40 == 0 :
                view_data = ""
                for x in range(640) :
                    xy = xy + 1
                    if x % 20 == 0 :
                        if data_data_all[xy]  > limit : view_data += " "
                        if data_data_all[xy] <= limit : view_data += " 1234567899"[int(data_data_all[xy])//int(limit/10)]
                view_data_all.append(view_data)
                
                if y >= 0 and y < 360 :
                    for a in range(1,32):
                        if view_data[a] == " " : add_num = add_num 
                        else : add_num = add_num + int(view_data[a])
                    # for a in range(1,3):
                    #     if view_data[a] == " " : add_edge_num = add_edge_num
                    #     else : add_edge_num = add_edge_num + int(view_data[a])
                    # for a in range(13,32):
                    #     if view_data[a] == " " : add_edge_remain_num = add_edge_remain_num
                    #     else : add_edge_remain_num = add_edge_remain_num + int(view_data[a])
                    for a in range(30,32):
                        if view_data[a] == " " : add_edge_num = add_edge_num
                        else : add_edge_num = add_edge_num + int(view_data[a])
                    for a in range(1,20):
                        if view_data[a] == " " : add_edge_remain_num = add_edge_remain_num
                        else : add_edge_remain_num = add_edge_remain_num + int(view_data[a])

        for y in range(12):
        # for y in range(6):
            print(view_data_all[y])   

        my_angle = int(yaw_z)
        my_distance = math.sqrt((position_x * position_x) + (position_y * position_y))

        error_angle = 11
        error_distance = 0.64

        my_add_error_angle = my_angle + error_angle
        my_add_error_distange = my_distance + error_distance

        ## 매핑 시작 
        ## ( 매핑준비중 = 1m 이상 움직이기 전)
        if mapping == "매핑준비중" or mapping == "매핑진행중": 
            # if add_edge_num == 0 :
            #     if add_edge_remain_num == 0 :
            #         speed = speed - 0.007
            #         angle = angle + 0.007
            #     if add_edge_remain_num >  0 :
            #         speed = speed - 0.007
            #         angle = angle - 0.007
            # if add_edge_num  > 0 :
            #     if add_edge_remain_num == 0 :
            #         speed = speed + 0.02
            #         if angle >  0.01 : angle = angle - 0.007
            #         if angle < -0.01 : angle = angle + 0.007
            #     if add_edge_remain_num >  0 :
            #         speed = speed - 0.0015
            #         angle = angle - 0.007
            if add_edge_num == 0 :
                if add_edge_remain_num == 0 :
                    speed = speed - 0.007
                    angle = angle - 0.007
                if add_edge_remain_num >  0 :
                    speed = speed - 0.007
                    angle = angle + 0.007
            if add_edge_num  > 0 :
                if add_edge_remain_num == 0 :
                    speed = speed + 0.02
                    if angle >  0.01 : angle = angle - 0.007
                    if angle < -0.01 : angle = angle + 0.007
                if add_edge_remain_num >  0 :
                    speed = speed - 0.0015
                    angle = angle + 0.007

        if mapping == "매핑준비중" and my_distance > 1 : mapping = "매핑진행중"
            
        ## ( 매핑진행중 =  1m 이상 움직인 후 매핑 진행중)
        if mapping == "매핑진행중" and my_add_error_distange < 0.3 :
            speed = 0
            angle = 0
            mapping = "매핑종료"

        ## ( 매핑종료 = 매핑이 끝난 후 처음위치 10cm 이내 도착시 정지 및 각도조절 )
        if mapping == "매핑종료" :
            if not(my_add_error_angle == 0) :
                if my_add_error_angle > 0  : angle = -0.3
                if my_add_error_angle < 0  : angle =  0.3
            if    (my_add_error_angle == 0) : 
                angle = 0
                mapping = "매핑완료"

        ## ( 매핑완료 = 매핑종료 후 사물QR 대기 )
        if mapping == "매핑완료" :
            if barcode_data_product_QR != "QR_X" : 
                qr_moving = "QR진행중"
                qr_moving_step = "각도변경중"
                if qr_target == "QR_X":
                    if barcode_data_product_QR == "A": qr_target = "QR_A"
                    if barcode_data_product_QR == "B": qr_target = "QR_B"
                    if barcode_data_product_QR == "C": qr_target = "QR_C"
                    
            if qr_moving_step == "출발지복귀중" and barcode_data_product_QR == "QR_X" : qr_target = "QR_X"


            if qr_moving == "QR진행중" :

                ## AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                if qr_target == "QR_A" :
                    if qr_moving_step == "각도변경중" : 
                        if not(abs(my_add_error_angle - QR_A_angle) < 10) : 
                            if (my_add_error_angle - QR_A_angle) > 0 : angle = -0.15
                            if (my_add_error_angle - QR_A_angle) < 0 : angle =  0.15
                        if    (abs(my_add_error_angle - QR_A_angle) < 10) :
                            angle = 0
                            qr_moving_step = "목적지이동중"

                    if qr_moving_step == "목적지이동중":
                        if not(abs(QR_A_distance - my_add_error_distange) < 0.1) : speed = 0.3
                        if    (abs(QR_A_distance - my_add_error_distange) < 0.1) :
                            speed = 0
                            qr_moving_step = "출발지복귀중"
                            
                ## BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
                if qr_target == "QR_B" :
                    if qr_moving_step == "각도변경중" : 
                        if not(abs(my_add_error_angle - QR_B_angle) < 10) : 
                            if (my_add_error_angle - QR_B_angle) > 0 : angle = -0.15
                            if (my_add_error_angle - QR_B_angle) < 0 : angle =  0.15
                        if    (abs(my_add_error_angle - QR_B_angle) < 10) :
                            angle = 0
                            qr_moving_step = "목적지이동중"

                    if qr_moving_step == "목적지이동중":
                        if not(abs(QR_B_distance - my_add_error_distange) < 0.1) : speed = 0.3
                        if    (abs(QR_B_distance - my_add_error_distange) < 0.1) :
                            speed = 0
                            qr_moving_step = "출발지복귀중"
                        
                ## CCCCCCCCCCCCCCCCCCCCCCCCCCC
                if qr_target == "QR_C" :
                    if qr_moving_step == "각도변경중" : 
                        if not(abs(my_add_error_angle - QR_C_angle) < 10) : 
                            if (my_add_error_angle - QR_C_angle) > 0 : angle = -0.15
                            if (my_add_error_angle - QR_C_angle) < 0 : angle =  0.15
                        if    (abs(my_add_error_angle - QR_C_angle) < 10) :
                            angle = 0
                            qr_moving_step = "목적지이동중"

                    if qr_moving_step == "목적지이동중":
                        if not(abs(QR_C_distance - my_add_error_distange) < 0.1) : speed = 0.3
                        if    (abs(QR_C_distance - my_add_error_distange) < 0.1) :
                            speed = 0
                            qr_moving_step = "출발지복귀중"
                        
                ## 공통 ##################
                if  qr_moving_step == "출발지복귀중" and qr_target == "QR_X":
                    run_direction = "후면"
                    if not(abs(my_add_error_distange) < 0.3) : speed = -0.3
                    if    (abs(my_add_error_distange) < 0.3) :
                        speed = 0
                        qr_moving_step = "행동초기화중"

                if qr_moving_step == "행동초기화중" :
                    run_direction = "정면"
                    if not(my_add_error_angle == 0) : angle = -0.3
                    if    (my_add_error_angle == 0) : 
                        angle = 0
                        qr_moving_step = "QR대기중"
                        qr_moving = "QR대기중"
                        qr_target = "QR_X"



        if angle > 0.4 : angle = 0.4
        if angle < -0.4 : angle = -0.4
        if speed > 0.25 : speed = 0.25
        if speed < 0 and run_direction == "정면" : speed = 0

        print("--------------------------------")
        print("speed : ",speed)
        print("angle : ",angle)
        
        # print("X 위치값 : ", position_x)
        # print("Y 위치값 : ", position_y)


        # print("상하 각도 : ", pitch_y*(-1))
        print("mapping : ", mapping)
        # print("qr_target : ", qr_target)
        # print("qr_moving : ", qr_moving)
        # print("qr_moving_step : ", qr_moving_step)
        # print("barcode_data_product_QR :", barcode_data_product_QR)
        # print("run_direction :", run_direction)
        print("my_angle : ", my_angle)
        print("my_distance :", my_distance)
        print("my_add_error_angle : ", my_add_error_angle)
        print("my_add_error_distange :", my_add_error_distange)
        # print(orientation_x, orientation_y, orientation_z, orientation_w)
    except :
        speed = 0
        angle = 0

    talker()
        
        
def talker():
    # rospy.init_node("project3",anonymous=True)
    
    # while not rospy.is_shutdown():
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    msg = Twist()
    msg.linear.x = speed
    msg.angular.z = angle
    pub.publish(msg)

    
def listen():
        rospy.init_node("project3",anonymous=False)
        rospy.Subscriber("/camera/depth/image_rect_raw",Image,cam_lidar_read)
        rospy.Subscriber("/odom",Odometry,lidar_pose)
        
        rospy.spin()

if __name__ == "__main__":
    try:
        listen()

    except rospy.ROSInterruptException:
        print('error')
        pass