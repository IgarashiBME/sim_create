#!/usr/bin/python
# -*- coding:utf-8 -*-

import rospy
import sys
import select
import termios
import time

from geometry_msgs.msg import Twist

velocity_x = 0.5
angular_z = 0.5

def teleop():
    while not rospy.is_shutdown():
        kb = input()
        twist = Twist()
    
        if str(kb) == 'q':
            print("exit")
            exit()

        elif str(kb) == "w":
            twist.linear.x = velocity_x; twist.linear.y = 0; twist.linear.z = 0;
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0;
            pub.publish(twist)

        elif str(kb) == "a":
            twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0;
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = angular_z;
            pub.publish(twist)

        elif str(kb) == "s":
            twist.linear.x = -velocity_x; twist.linear.y = 0; twist.linear.z = 0;
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0;
            pub.publish(twist)

        elif str(kb) == "d":
            twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0;
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = -angular_z;
            pub.publish(twist)

        time.sleep(0.01)

def input():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~termios.ICANON
    new[3] &= ~termios.ECHO

    try:
        termios.tcsetattr(fd, termios.TCSANOW, new)
        i,o,e = select.select([sys.stdin],[],[], 0.1)
        if (i):
            key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)

    if (i):
        return key
    else:
        return None   

if __name__=="__main__":
    pub = rospy.Publisher('/sim_create/diff_drive_controller/cmd_vel', Twist, queue_size = 1)
    rospy.init_node('teleop_twist_keyboard')
    print "ready to sim_keyboard_teleop"
    print "w:forward\n\r a:left\n\r s:backward\n\r d:right"

    teleop()
