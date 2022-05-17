#!/usr/bin/python
#_*_ coding: utf8 _*_
import pyzbar.pyzbar as pyzbar
import cv2
import rospy
from geometry_msgs.msg import Twist
import time

cap = cv2.VideoCapture(0)

code = "A"
code_1 = "B"
code_2 = "C"

def talker():
    rospy.init_node("yh_turtle_move")
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 100)
    msg = Twist()
    while not rospy.is_shutdown():
        global cap
        pub.publish(msg)
        retval, frame = cap.read()
        if not retval:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #QR과 바코드를 정확히 인식하기 위해, BGR에서 1채널 Gray로 변경
        decoded = pyzbar.decode(gray) # QR을 인식하는 함수 print(decoded)해보면 QR을 나눴을 때, 어떤 정보가 나오는지 알 수 있음.
        for d in decoded: # decoded 정보를 변수 d에 넣음 으로써 루프를 돌림. 
            x, y, w, h = d.rect # QR을 인식할때 시각적으로 QR코드의 사각형을 만듬
            barcode_data = d.data.decode("utf-8") #QR 안에 들어있는 정보들을 저장시켜놓음
            barcode_type = d.type # 인식하고 있는것이 QR인지 barcode인지 알 수 있음.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) # OpenCv를 통해서 QR코드를 인식할 때, 사각형을 시각적으로 보여주고 색상까지 정할 수 있음
            text = '%s (%s)' % (barcode_data, barcode_type) # QR코드 안에 어떤 정보인지, 어느 타입인지 문구를 통해 알 수 있게 함
            cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA) # openCv를 통해 QR코드 안에 정보와 타입을 시각적으로 표현할 수 있게 한다.

        if decoded != [] and code == "A": # QR을 인식하게 되면 decoded의 정보들이 배열 안에 들어 가기 때문에, 빈 배열이 아니라면 움직이게 만든다.
            msg.angular.z = 0
            msg.linear.x = 0
        # if decoded == [] : # QR을 인식 안할 때는 decoded의 정보가 빈 배열이기 때문에, QR을 인식하지 않으면 움직이지 않게 만든다.
        #     msg.angular.z = 0

        if decoded != [] and code_1 == "B":
            msg.angular.z = 0
            msg.linear.x = 0
        
        if decoded != [] and code_2 == "C":
            msg.angular.z = 0
            msg.linear.x = 0


        key = cv2.waitKey(25)
        cv2.imshow('frame', frame)
        if key == ord('q'):
            break 
if __name__ == "__main__":
    try:
        talker()
    except rospy.ROSInterruptException:
        pass