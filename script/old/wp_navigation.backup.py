#!/usr/bin/env python                                                            
# -*- coding: utf-8 -*-                                                          

import rospy
import tf
import actionlib
import numpy as np

from nav_msgs.msg import Odometry
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion\
, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import pi

Straight_Dist = 4
Straight_Split = 10
Round_Trip_Times = 3
Dist_Line = 0.2

class WpNavi():
  def __init__(self):  # コンストラクタ                                        
    # ノードの初期化                                                         
    rospy.init_node('wp_navi')

    # シャットダウン時の処理                                                 
    rospy.on_shutdown(self.shutdown)

    # robot position
    rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.callback_amcl_pose)
    self.robot_pose = [0, 0]
    self.robot_quaternion = [0, 0, 0, 0]

  def callback_amcl_pose(self, data):
    self.robot_pose[0] = data.pose.pose.position.x
    self.robot_pose[1] = data.pose.pose.position.y
    self.robot_quaternion[0] = data.pose.pose.orientation.x
    self.robot_quaternion[1] = data.pose.pose.orientation.y
    self.robot_quaternion[2] = data.pose.pose.orientation.z
    self.robot_quaternion[3] = data.pose.pose.orientation.w
    self.robot_euler = tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w))
    self.robot_yaw = self.robot_euler[2]

    #print self.robot_euler

  def run(self):
    # アクションクライアントの生成                                           
    self.ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    # アクションサーバーが起動するまで待つ。引数はタイムアウトの時間(秒）    
    while not self.ac.wait_for_server(rospy.Duration(5)):
      rospy.loginfo("Waiting for the move_base action server to come up")

    rospy.loginfo("The server comes up");

    # ゴールの生成                                                           
    self.goal = MoveBaseGoal()
    self.goal.target_pose.header.frame_id = 'map' # robot座標系       
    self.goal.target_pose.header.stamp = rospy.Time.now() # 現在時刻         

    distance = 2.5 
    x = np.cos(self.robot_yaw) * distance + self.robot_pose[0]
    y = -np.sin(self.robot_yaw) * distance + self.robot_pose[1]
    #way_point = [[x, y, self.robot_yaw], [0, 0, 0], [999, 999, 999]]
    way_point = []
    way_point.append([x, y, self.robot_yaw])

    print way_point 

    # メインループ。ウェイポイントを順番に通過                               
    i = 0
    while not rospy.is_shutdown():
      # ROSではロボットの進行方向がx座標、左方向がy座標、上方向がz座標     
      self.goal.target_pose.pose.position.x =  way_point[i][0]
      self.goal.target_pose.pose.position.y =  way_point[i][1]

      if way_point[i][0] == 999:
        break

      q = tf.transformations.quaternion_from_euler(0, 0, way_point[i][2])
      self.goal.target_pose.pose.orientation = Quaternion(q[0],q[1],q[2],q[3])
      rospy.loginfo("Sending goal: No" + str(i+1))

      # サーバーにgoalを送信                                               
      self.ac.send_goal(self.goal);

      # 結果が返ってくるまで120.0[s] 待つ。ここでブロックされる。           
      succeeded = self.ac.wait_for_result(rospy.Duration(120));
      # 結果を見て、成功ならSucceeded、失敗ならFailedと表示                
      state = self.ac.get_state();

      if succeeded:
        rospy.loginfo("Succeeded: No."+str(i+1)+"("+str(state)+")")
        #i = i + 1
      else:
        rospy.loginfo("Failed: No."+str(i+1)+"("+str(state)+")")

      i = i + 1

  def shutdown(self):
    rospy.loginfo("The robot was terminated")
    # ゴールをキャンセル                                                     
    self.ac.cancel_goal()

if __name__ == '__main__':
  try:
    WpNavi()
    WpNavi().run()
    rospy.spin()
  except rospy.ROSInterruptException:
    rospy.loginfo("WP navigation finished.")

