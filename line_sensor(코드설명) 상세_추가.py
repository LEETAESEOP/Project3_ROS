#!/usr/bin/python3
# -*- coding: utf-8 -*-

## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

from geometry_msgs.msg import Twist # ROS 움직임을 위한 메세지
import pyzbar.pyzbar as pyzbar # QR코드 읽는 것에 대한 라이브러리
from datetime import datetime 
import pyrealsense2 as rs #LIDAR 센서의 읽힘을 위한 라이브러리
import numpy as np
import schedule
import rospy # ROS를 사용하기 위한 라이브러리 
import time
import cv2 #opencv를 사용하기 위한 라이브러리

##변수 값들

#크롭 영역(라인 추적 영역)
#카메라 프레임 안에 빨간 사각형을 그려 그 안에서 라인추적을 하기 위한 틀

#frame_crop_변수값들의 점을 찍어 놓고 사각형을 그릴 것임

frame_crop_x1 = 0 # 사각형 중 가로 왼쪽 점에 대한 값
frame_crop_y1 = 120 #사각형 중 세로 왼쪽 점에 대한 값
frame_crop_x2 = 639 # 사각형중 가로 오른쪽 점에 대한 값
frame_crop_y2 = 479 # 사각형중 세로 오른쪽 점에 대한 값

minLineLength = 30 #선을 검출 하기 위한 최소 단위 만약 선을 검출 했을 때, 이 값 보다 낮으면 검출이 안됨
maxLineGap = 15 # 선과 선사이의 최대 허용 간격, 이 값보다 작으면 값이 들어가지 않는다.

speed = 0   #RC카의 linear.x 직진을 위한 변수 값
angle = 0 #RC카의 angular.z 회전을 위한 변수 값
avr_x = 0 
rccar_stop = 0
turn = 0.5 # RC카의 방향을 정하는 변수 값, 나중에 angle 값에 turn 값을 넣어 회전을 시킬 때, 각도를 조절함
left_view = 1 # 장애물의 유무

code_start = "start"
barcode_data_line_QR = [] #barcode를 찍었을 때, qrcode의 대한 많은 정보가 list로 들어오게 되는데, 변수로 이것을 초기화 시켜둠
text_0 = "" #barcode 정보에 대한 text(문자열) 
text_1 = "" #barcode 정보에 대한 text(문자열)

## 시간제어 변수
prev_time = 0
next_time = 0
count_second = 0 
obstacle_view = 0

cap_0 = cv2.VideoCapture(2) #RC카 line_detector과 QRcode의 인식을 위한 cam 변수
cap_1 = cv2.VideoCapture(4) #RC카 물건 여부 QRcode의 인식을 위한 cam 변수

cap_1.set(cv2.CAP_PROP_FRAME_HEIGHT,180) # cap_1 번에 대한 프레임 값을 지정해주는 함수(세로)
cap_1.set(cv2.CAP_PROP_FRAME_WIDTH,320)  # cap_1 번에 대한 프레임 값을 지정해주는 함수(가로)

def cam_0_read(): #line_detector와 qrcode를 인식하기 위한 함수(전역 변수를 둬서 어디서든 사용할 수 있게 함)
    global retval_0, frame_0, original, gray_line_0, gray_line_1
    retval_0, frame_0 = cap_0.read() # cam에 대해 opencv 안의 read 함수를 써서 읽어 올 수 있게 함
    original = frame_0 #original 이라는 변수를 둬서 cam의 원본을 훼손하지 않고 사용할 수 있게 됨
    gray_line_0 = cv2.cvtColor(frame_0, cv2.COLOR_BGR2GRAY) # line_detector 의 화면을 gray 컬러(2채널)로 바꿈
    gray_line_1 = cv2.cvtColor(frame_0, cv2.COLOR_BGR2GRAY) # qrcode의 사용 될 화면을 gray 컬러(2채널)로 바꿈

def cam_1_read(): # cam_1은 나중에 나오는 qr_product만을 찍기 위한 변수 인데  이것을 읽기 위한 함수지정
    global retval_1, frame_1, gray_product_0
    retval_1, frame_1 = cap_1.read() # cam_0_read에 대해 설명과 동일
    gray_product_0 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY) #cam_0_read에 대해 설명과 동일

def cam_0_use_line(): # 전에 cam에 대해 read 하는 것을 썼으니 이제 어떻게 사용할 것인지에 대한 함수
    global retval_0, frame_0, original, theta
    
    #blurred라는 변수를 둬서 화면을 frame_crop 값을 사용하여 화면을 어떻게 자를 것인지에 대한 내용
    #frame_crop대해 값을 바꿔서 실행하면 화면을 어떻게 구성할 것인지 선택할 수 있음 ex)[160:320, 0:130] <- 화면을 어떻게 자를 것인 가 에 대한 내용
    blurred = gray_line_0[frame_crop_y1:frame_crop_y2,frame_crop_x1:frame_crop_x2]
    
    blurred = cv2.boxFilter(blurred, ddepth=-1, ksize=(31,31)) #opencv 함수를 사용 ksize를 조절하면 화면의 부드러워짐(혹은 뭉게짐)을 조절가능
    
    # 앞전 코드에 cam을 gray(2채널)컬러로 바꾸었는데 이것을 threshold(임계값)을 사용해 화면 색이 100보다 낮으면 검은색, 100보다 높으면 흰색으로 바꿈
    retval2 ,blurred = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
     
    edged = cv2.Canny(blurred, 85, 85) #canny는 opencv 함수 중 선 검출하는 함수이다. 앞전 코드인 blurred 변수 값을 가져오고 canny 85,85 처럼 숫자를 바꾸면 선을 얼마나 검출 할 것인지를 바꿀수 있음
    lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap) #opencv 내 양 끝 점에 있는 선분을 검출하는 함수이다. 
    max_diff = 1000 #변수 값
    final_x = 0 #마지막 선 검출에 대한 변수 값
    if ( lines is not None ): #만약 line들이 검출이 된다면
        if ( lines is not None ):
            add_line = 0 # line의 값을 더한다는 의미를 가진 변수 선언
            for line in lines: # 위에 lines에 대한 값을 line에 넣고 반복문을 돌림
                x1, y1, x2, y2 = line[0] #print(line[0])을 찍어보면 x1,y1,x2,y2에 대한 값이 리스트로 나오게 됨
                
                #cv2.line은 검출 된 값을 선으로 표현하는 함수, 이것을 실행 시키면 영상에 검출된 선들이 녹색으로 표현되어 나온다. ex)x1 =100,frame_crop_x1 = 0 이라면, 화면이 640x320이니 그 값에 맞게 검출된 선 값이 화면 값에 맞춰 표현됨
                cv2.line(original,(x1+frame_crop_x1,y1+frame_crop_y1),(x2+frame_crop_x1,y2+frame_crop_y1),(0,255,0),3)
                mid_point = ( x1 + x2 ) / 2 #mid_point 변수를 지정해 놓음, ex) 선에 캠으로 라인을 찍으면 print(x1,x2) 값이 나오는데 그것을 나누기 2하여 x1,x2에 대한 값의 평균을 냄
                diff = abs((640/2) - mid_point) #diff라는 변수를 두고 프레임 값이 640이였으니, 640의 중간을 맞추기 위해, /2 한다.
                if ( max_diff > diff ) : # max_diff = 1000이라고 지정해 줬는데 diff은 절대로 max_diff을 넘을 수가 없음. print(diff)을 통해 값을 보면 된다. 무조건 실행되는 if문임
                    max_diff = diff #max_diff은 diff가 되고
                    final_x = mid_point #final_x = 0이라고 지정해줬지만 그것이 mid_point의 값이 되고
                add_line = add_line + final_x #add_line을 0이라고 지정해줬지만 그것은 반복문을 통해 계속 값이 늘어 난다.
            average_x = add_line / len(lines) #average_x를 변수로 지정하고 add_line의 값이 계속 커지는데 검출된 len(lines)를 나누니, 평균치가 된다. 평균이 된다면, 검출 된 값이 튀어도(한번 갑자기 값이 낮아지거나, 커져도) 평균값에 크게 변화를 주지 않기 때문에 나중에 나오는 theta 값에 큰 영향 주지 않음
        if ( int(average_x) != 0 ) : #average_x는 원래 float으로 나오는데 int로 바꿔서 값을 계산하기 편하게함
            
            #cv2.circle은 int(average)가 0이 아니라면 빨간색 원을 만들어 라인들의 평균들을 그림으로 대충 볼 수 있게 만듬
            original = cv2.circle(original,(int(average_x),int((frame_crop_y1+frame_crop_y2)/2)),5,(0,0,255),-1)
            #cv2.rectangle은 frame_crop들의 변수 값들을 활용해 cam 프레임에 맞춰서 빨간 사각형(line 값이 검출되는)을 만들다
            original = cv2.rectangle(original,(int(frame_crop_x1),int(frame_crop_y1)),(int(frame_crop_x2),int(frame_crop_y2)),(0,0,255),1)
        frame_0 = original
        theta = int(( int(average_x) - 320.0 ) / 640.0 * 100) #필자는 필자가 그려놓은 라인의 모양에 맞춰 theta값을 맞췄음. theta는 -50부터 50이 라인이 벗어나지 않는 것임, average_x값에 화면의 중간(640/2= 320)을 빼고, 화면 가로크기(640)*100을 하면 line이 검출될 때 theta는 -50 ~ 50의 값이 나옴 
    if ( lines is None ): #라인이 검출되지 않는다면 theta 값을 -50으로 두어 , 나중에 theta 값에 맞춰 rc카가 line에 맞출수 있도록 할 예정임
        
        theta = -50

def cam_0_use_qrcode(): #cam_0(line_detector과 qrcode를 읽는 캠)을 사용하게 할 것이라는 함수
    global barcode_data_line_QR, barcode_type_line_QR
    decoded_line_QR = pyzbar.decode(gray_line_1) #pyzbar.decode는 qr코드가 인식되면 qr코드의 값에 대한 내용이 나오는데 이것을 decoded_line_QR이라는 함수에 넣는다
    for _ in decoded_line_QR: # 반복문안에 qrcode 데이터가 들어가있다면 실행함
        x, y, w, h = _.rect # x,y,w,h 변수 안에 값을 준다. 사각형을 만들기 위한 값
        barcode_data_line_QR = _.data.decode("utf-8") # 유니코드를 사용하여 data를 추출 한다
        barcode_type_line_QR = _.type # 읽어온 것이 QR코드인지 barcode인지 type을 알려준다
        cv2.rectangle(frame_0, (x, y), (x + w, y + h), (0, 0, 255), 2) # cam의 frame 안에 QR코드가 있다면 그것을 사각형으로 표현해준다
        text_0 = '%s (%s)' % (barcode_data_line_QR, barcode_type_line_QR) # QR코드에 대한 정보, type을 text로 만든다.
        cv2.putText(frame_0, text_0, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA) # 제공된 프레임안에 text를 text의 색깔, 두께 등을 맞추어 보기 좋게 표현한다.
    if decoded_line_QR == [] : # 만약 cam에 QR코드가 읽히지 않는다면
        barcode_data_line_QR = "QR_X" # "QR_X" 라는 변수를 만들어 준다.

def cam_1_use_qrcode(): #cam_1(product)의 QR인식 내용 (QR의 인식하는 내용은 cam_0_use_qr코드와 동일하다.)
    global barcode_data_product_QR, barcode_type_product_QR #上同
    decoded_product_QR = pyzbar.decode(gray_product_0) #上同
    for _ in decoded_product_QR: #上同
        a, b, c, d = _.rect #上同
        barcode_data_product_QR = _.data.decode("utf-8") #上同
        barcode_type_product_QR = _.type #上同
        cv2.rectangle(frame_1, (a, b), (a + c, b + d), (0, 0, 255), 2) #上同
        text_1 = '%s (%s)' % (barcode_data_product_QR, barcode_type_product_QR) #上同
        cv2.putText(frame_1, text_1, (a, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA) #上同
    if decoded_product_QR == [] : #上同
        barcode_data_product_QR = "QR_X" #上同

def cam_lidar_read():
    global pipeline
    pipeline = rs.pipeline() # 컨텍스트 변수를 만듭니다. 이 변수는 연결된 모든 실제 감지 장치를 조절함
    config = rs.config() #stream 구성
    config.enable_stream(rs.stream.depth, 320, 240, rs.format.z16, ) # 가로(x)= 320 * 세로(y)= 240의 화면으로 구성하겠다.
    pipeline.start(config) #스트리밍 시작

def cam_lidar_use():
    global add_num, add_edge_num, add_edge_remain_num, image_all, left_view
    frames = pipeline.wait_for_frames() 
    depth = frames.get_depth_frame()
    coverage = [0]*32 # [0,0,0,0,0,0,0,0,0,....] []배열안에 0이 32개 있음
    image_all = [] 
    add_num = 0
    add_edge_num = 0
    add_edge_remain_num = 0
    for y in range(240): # config.enable_stream 코드에서 320*240으로 화면을 맞췄기 때문에 coverage(적용범위)맞춰줌 enable 코드에 썼던 숫자와 맞추지 않으면 실행 안됨
        for x in range(320):
            dist = depth.get_distance(x, y) 
            if 0 < dist and dist < 1: # dist = m 단위임. 범위는 0m ~ 1m 까지 depth 적용됨
                coverage[x//10] += 1 # coverage[32] = coverage[32] + 1
                # 위 coverage = [0,0,0,0....0,0,0,0] 의 형식으로 리스트안에 총 32개의 값이 저장됨
                # 위 coverage 32개의 각각의 값은 최소 0 ~ 200 까지 값을 가질 수 있음.
                # 그 이유는 coverage의 1개의 값은 x범위 10개, (아래 y%20 의미가) y범위 20개를 가지기 때문임.
        if y%20 is 19:
            line = ""
            for c in coverage:
                line += " 12345678"[c//25]  # 각 coverage값을 " 12345678"로 매칭시킴.
                # coverage = [0, 30, 65, 80, 110... 174, 200]일 경우에 line = ' 1234...78' 값을 가지게 된다.
            coverage = [0]*32       # coverage 초기화
            image_all.append(line)  # y가 0~19 만큼 진행됬을때 image_all = ['01234...88']
                                    # y가 0~59 까지 진행됬을때 image_all = ['01234...88', '.......', '.......'] 의 총 3개의 line값을 가지게 된다.
                                    # y가 0~240 까지 진행됬을때 image_all = 총 12개의 line값을 가지게 된다.
            for a in range(1,32):
                if line[a] == " " : add_num = add_num       # line[a] 값이 " " 이면, add_num 값은 그대로다.
                else : add_num = add_num + int(line[a])     # line[a] 값이 "1"or"2"or..."7"or"8" 이면, add_num 값을 누적시킨다.
            for a in range(1,2):
                if line[a] == " " : add_edge_num = add_edge_num # 위와 같은 형태이며, 변수 add_edge_num 값을 누적시킨다. (벽타기에 활용변수)
                else : add_edge_num = add_edge_num + int(line[a]) 
            for a in range(3,32):
                if line[a] == " " : add_edge_remain_num = add_edge_remain_num # 위와 같은 형태이며, 변수 add_edge_remain_num 값을 누적시킨다. (벽타기에 활용변수)
                else : add_edge_remain_num = add_edge_remain_num + int(line[a])
    
    

def speed_and_angle_make():
    global angle, speed # 위에 있던 변수 값들을 기억한다면 무슨 말인지 알수 있다.
    
    #원본(round(((-theta *1.8) * (np.pi / 180 radian = 0.01 (각 1도)) / 3 * 2), 2)) 
    angle = round((-theta) * (0.015), 2) #angle은 회전을 위한 변수이고, theta가 음수라면 오른쪽, 양수면 왼쪽으로 rc카가 돌것이다. 화면의 중앙과 line을 찾기 위해서. round 함수는 소수점 까지 표현 하겠다는 함수
    speed = 0.3 - abs(angle * 0.2) #speed는 앵글 값에 비례해 달라질 수 있도록 변수를 만듬

def speed_and_angle_zero(): # speed, angle의 속도와 각도를 0으로 만들겠다는 함수
    global angle, speed, rccar_stop
    speed = 0      
    angle = 0                              
    rccar_stop = 1

def speed_and_angle_turn(): # turn을 인식했을 때, angle은 turn으로 된다는 함수
    global angle, speed
    speed = 0      
    angle = turn

def speed_and_angle_main():
    global angle, speed, barcode_data_product_QR, barcode_data_line_QR, turn, obstacle_view, view_same_QR, view_start_QR_and_no_product
    
    if barcode_data_line_QR == "turn"  : turn = -0.5 #QR코드 인식 된 내용이 turn 이라면 angle이 turn인 -0.5가 된다
    if barcode_data_line_QR == "start" : turn = 0.5 #QR코드 인식 된 내용이 start 라면 angle이 turn인 0.5가 된다

    if view_same_QR == 0 and view_start_QR_and_no_product == 0 : #view_same_QR : QR코드가 같은 것일 때라는 변수, view_start_QR_and_no_product : 'start' QR을 보고, RC카에 물건 QR이 없을 때 
        if obstacle_view == 0 : #장애물이 없을 때,
            if theta != -50:  #theta가 -50이 아닐 때, 즉, 라인이 인식 되었을때,
                if add_num <= 10                                                                                           : speed_and_angle_make() #장애물 인식 변수인 add_num가 10보다 작다면(장애물이 없다면), speed_and_angle_make()의 내용을 따른다.
                if add_num <= 10 and barcode_data_product_QR != "QR_X" and barcode_data_product_QR == barcode_data_line_QR : view_same_QR = 1 #장애물인식이 안되고, 물건의 QR코드를 인식되고, 물건QR과 레일의 QR코드 내용과 일치하게 된다면
                if add_num <= 10 and barcode_data_product_QR == "QR_X" and barcode_data_line_QR    == "start"              : view_start_QR_and_no_product = 1 #장애물 인식이 안되고, 물건의 QR코드가 없거나, 레일 위 QR코드가 "start"라면 
                if add_num >  10 : #장애물이 인식이 된다면
                    speed = 0 # 속도는 0이되고
                    obstacle_view = 1 #장애물 인지를 하게 된다.
            if theta == -50 : speed_and_angle_turn() # 레일 인식이 되지 않는다면, 함수내용 대로 행동하게 된다.
                
        if obstacle_view == 1 : #장애물이 인지가 되었을 때,
            if add_num != 0 : #장애물이 인지가 되었을 때, 
                if add_edge_num        > 0 and add_edge_remain_num == 0 : angle = -0.4 # edge_num이 인식되고, remain 장애물 인지가 안될 때, 오른쪽으로 튼다.
                if add_edge_remain_num > 0 and add_edge_num == 0 : angle = -0.4 #remain 장애물이 있고, edge_num에 장애물이 없어도, 오른쪽으로 튼다. ex) 사물이 있으면, 계속 오른쪽으로 트는 구조
                if add_edge_remain_num > 0 and add_edge_num > 0 : angle = -0.4 # remain에 장애물이 있고, edge_num에 장애물이 있어도, 오른쪽으로 튼다.
                speed = 0.2  #속도는 0.2만큼 지정해줌, 앞전 코드와 같이 angle과 speed 비례로 하게되면 속도가 너무 빨라지기 때문에 
            if add_num == 0                  : angle = 0.4 # 장애물 인지가 아예 안됐을 땐,rc카를 왼쪽으로 틀어 라인을 인식 할 수 있도록 한다. , 필자들의 설정에 맞춘 것으로 언제든지 바꿀 수 있음.
            if theta != -50 and add_num == 0 : obstacle_view = 0  # 라인 인식이 되고, 장애물 인식이 안될 때, obstacle_view는 0이 되고, 앞전 코드 인 obstacle_view == 0 인 if문으로 넘어가서 실행이 된다.

    if view_same_QR == 1 or view_start_QR_and_no_product == 1: #QR 코드가 같게 되고, QR코드가 start를 보면서, 물건QR이 없게된다면
        speed = 0 # 멈춤
        angle = 0 # 멈춤
        if view_same_QR == 1                 and barcode_data_product_QR == "QR_X" : view_same_QR = 0 # 변수가 1이 되고, 물건 QR이 없으면, 초기화
        if view_start_QR_and_no_product == 1 and barcode_data_product_QR != "QR_X" : view_start_QR_and_no_product = 0 #변수가 1이 되고, 물건이 있으면 초기화


def talker(): # ros rc카 구동을 위한 publisher를 넣어놓은 함수 
    global rccar_stop, speed, angle, count_second
    rospy.init_node("line_qr_sensor") # node 이름을 정해서 헷갈리지 않게 하자 
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10) # publisher를 통해 rc카의 움직임을 담당하는 /cmd_vel로 가서 message를 보내고, queud_size의 갯수를 지정한다.
    msg = Twist() # 읽는 그대로

    cam_lidar_read() # LIDAR sensor 작동하는 함수를 실행 시켜주고,

    while not rospy.is_shutdown(): #rospy가 꺼지지 않을 때 까지 계속 while 문을 실행 하겠다는 의미

        

        msg.linear.x = speed # message에 linear.x(직진)은 speed라고 지정한다. 
        msg.angular.z = angle # message에 angular.z(회전)는 angle이라고 지정한다.
        pub.publish(msg) # message를 publish한다. **제일중요함** message를 보내야 rc카를 정상적으로 구동할 수 있음.

        ## 함수를 실행시킬 때에는 어느정도 순서를 지켜주자, 함수내용에는 변수만 넣는 것도 있었고, 쓰는 내용만 있었기 때문에..while문도 차례대로 실행되는 구조이기 때문에, 순서대로 하는 것이 좋을 것 같다.
        cam_0_read() # 함수 실행
        cam_0_use_line() # 함수 실행 
        cam_0_use_qrcode() # 함수 실행

        cam_1_read() # 함수 실행
        cam_1_use_qrcode() # 함수 실행

        cam_lidar_use() # 함수 실행

        speed_and_angle_main() # 함수 실행

        for y in range(12):
            print(image_all[y])
        print(add_num)
        print("장애물 : ", obstacle_view)
        print("세타값 : ", theta)
        print("턴값 : ", turn)
        cv2.imshow('frame_0', frame_0)
        cv2.imshow('frame_1', frame_1)
        
        key = cv2.waitKey(25) #opencv 창을 띄웠을 때 키를 누르면 시간(25)만큼 뒤에 작동함 
        if key == 27: #ESC 일때, 종료함
            break

if __name__ == "__main__": ##__main__일 때 실행한다.
    try:
        talker() #talker()함수를 
    except rospy.ROSInterruptException: # 만약 실행할 때, rospy.ROSInterruptException 오류 뜨면, 이 오류는 예외시키고 실행시킨다는 말임.
        pass