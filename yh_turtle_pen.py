#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import rospy
from turtlesim.srv import SetPen

class TurtlePen:
    def __init__(self):
        self.client_pen = rospy.ServiceProxy("turtle1/set_pen", SetPen)
        # self.r = r
        # self.g = g
        # self.b = b
        # self.width = width
        # self.off = off

    def run(self):
       
        while not rospy.is_shutdown():

            r     = int(input     ("r값 : "))
            g     = int(input     ("g값 : "))
            b     = int(input     ("b값 : "))
            width = int(input ("width값 : "))
            off   = int(input   ("off값 : "))
            self.client_pen(r, g, b, width, off)

if __name__ == "__main__":
    rospy.init_node("yh_turtle_pen")
    turtle_pen = TurtlePen()
    turtle_pen.run()

# class TurtlePen:
#     def __init__(self):
#         self.client_pen = rospy.ServiceProxy("turtle1/set_pen", SetPen)
#         # self.r = r
#         # self.g = g
#         # self.b = b
#         # self.width = width
#         # self.off = off

#     def run(self):
#         while not rospy.is_shutdown():

#             r     = int(input     ("r값 : "))
#             g     = int(input     ("g값 : "))
#             b     = int(input     ("b값 : "))
#             width = int(input ("width값 : "))
#             off   = int(input   ("off값 : "))
#             self.client_pen(r, g, b, width, off)


# class t1(threading):

#     def __init__(self):
#         super().__init__()
#         self.t = threading.Thread(target=self.run)

#     def run(self):
#         turtle_pen.run()


# class t2(threading):

#     def __init__(self):
#         super().__init__()
#         self.t = threading.Thread(target=self.run)

#     def run(self):
#         turtle_pen.run()
    

# if __name__ == "__main__":
#     rospy.init_node("yh_turtle_pen")
#     turtle_pen = TurtlePen()

#     t = t1()
#     t.start()

    