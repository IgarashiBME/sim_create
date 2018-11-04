#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import rospy
import actionlib
import tf
from nav_msgs.msg import Odometry
import math
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


# ここに先のプログラムで出力されたリストを書き込む
csvdir = os.path.abspath(os.path.dirname(__file__))
os.chdir(csvdir)
f = open('route.csv', 'r')
reader = csv.reader(f)
line_count = 0
row_count = 0

waypoints = []
for row in reader:
    buf = []
    for data in row:
        line_count += 1
        buf.append(float(data))
        if line_count == 7:
            waypoints.append(buf)
            line_count = 0


def goal_pose(pose):
    goal_pose = MoveBaseGoal()
    goal_pose.target_pose.header.frame_id = 'map'
    goal_pose.target_pose.pose.position.x = pose[0]
    goal_pose.target_pose.pose.position.y = pose[1]
    goal_pose.target_pose.pose.position.z = pose[2]
    goal_pose.target_pose.pose.orientation.x = pose[3]
    goal_pose.target_pose.pose.orientation.y = pose[4]
    goal_pose.target_pose.pose.orientation.z = pose[5]
    goal_pose.target_pose.pose.orientation.w = pose[6]

    return goal_pose


if __name__ == '__main__':
    rospy.init_node('patrol')
    listener = tf.TransformListener()

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction) 
    client.wait_for_server()
    listener.waitForTransform("map", "base_link", rospy.Time(), rospy.Duration(4.0))

    while True:
        seq = 0
        for pose in waypoints:
            seq = seq +1
            goal = goal_pose(pose)
            client.send_goal(goal)
            while True:
                now = rospy.Time.now()
                listener.waitForTransform("map", "base_link", now, rospy.Duration(4.0))

                # map座標系の現在位置をｔｆから取得する
                position, quaternion = listener.lookupTransform("map", "base_link", now)

                # ウェイポイントのゴールの周囲１ｍ以内にロボットが来たら、次のウェイポイントを発行する
                succeeded = client.wait_for_result(rospy.Duration(10));
                # 結果を見て、成功ならSucceeded、失敗ならFailedと表示                
                state = client.get_state();

                if succeeded:
                    rospy.loginfo("Succeeded: No."+str(seq)+"("+str(state)+")")
                    break
                else:
                    rospy.loginfo("Failed: No."+str(seq)+"("+str(state)+")")
                """if(math.sqrt((position[0]-goal.target_pose.pose.position.x)**2 + (position[1]-goal.target_pose.pose.position.y)**2 ) <= 0.5):
                    print "waypoint" +str(seq), "finished"
                    break

                else:
                    rospy.sleep(0.5)"""
        print "finished"
        break
