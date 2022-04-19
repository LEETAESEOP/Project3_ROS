#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
from yh_sum.msg import yh_sum_msg

before_num = 0
def msgCallback(msg):

    global before_num
    rospy.loginfo("next_message: %d", msg.data)
    sum_result = before_num + msg.data
    rospy.loginfo("next_message + before_message: %d", sum_result)
    before_num = msg.data

def listener():
    
    rospy.init_node("yh_sum_sub", anonymous=True)
    rospy.Subscriber("yh_sum_topic", yh_sum_msg, msgCallback)

    rospy.spin()

if __name__ == "__main__":
    listener()
