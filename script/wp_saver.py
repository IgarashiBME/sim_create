#!/usr/bin/env python

import csv
import rospy
from move_base_msgs.msg import MoveBaseActionGoal

def callback(data):
    pos = data.goal.target_pose.pose

    f = open('route.csv', 'ab')
    csvWriter = csv.writer(f)
    waypoints = []

    # add position
    waypoints.append(pos.position.x)
    waypoints.append(pos.position.y)
    waypoints.append(pos.position.z)

    # add orientation
    waypoints.append(pos.orientation.x)
    waypoints.append(pos.orientation.y)
    waypoints.append(pos.orientation.z)
    waypoints.append(pos.orientation.w)
    csvWriter.writerow(waypoints)
    print "x:",pos.position.x, "y:",pos.position.y, "z:",pos.position.z
    print "qx:",pos.orientation.x, "qy:",pos.orientation.y, "qz:",pos.orientation.z, "qw:",pos.orientation.w
    f.close()

def listener():
    rospy.init_node('goal_sub', anonymous=True)
    rospy.Subscriber("/move_base/goal", MoveBaseActionGoal, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
