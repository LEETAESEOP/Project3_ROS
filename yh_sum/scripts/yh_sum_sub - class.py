#!/usr/bin/python
# _*_ coding: utf-8 _*_

import rospy
from topic_tutorial.msg import my_msg

class MyClass:

    def __init__(self):
        self.sub = rospy.Subsciber("yh_sum_topic", yh_sum_msg, self.msgCallback)
        self.old_data = 0

    def msgCallback(self, msg):
        print(self.old_data + msg.data)
        self.old_data = msg.data


def listener():
    rospy.init_node("py_subscriber", anonymous=T rue)
    my_class = MyClass()
    rospy.spin()        #종료하지않고 대기하게 하는 함수

if __name__ == "__main__":
    listener()