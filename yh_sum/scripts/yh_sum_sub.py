#!/usr/bin/python
# _*_ coding: utf-8 _*_

import rospy
from topic_tutorial.msg import my_msg

old_data = 0
def msgCallback(msg):
    global old_data
    print(old_data + msg.data)
    old_data = msg.data


def listener():
    rospy.init_node("py_subscriber", anonymous=True)
    rospy.Subscriber("my_topic", my_msg, msgCallback)

    rospy.spin()        #종료하지않고 대기하게 하는 함수

if __name__ == "__main__":
    listener()