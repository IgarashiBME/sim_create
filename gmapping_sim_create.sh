#!/bin/bash

gnome-terminal --geometry = 80x5+0+0 -e "/opt/ros/kinetic/bin/roslaunch sim_create gazebo.launch"

sleep 10

gnome-terminal --geometry = 80x5+0+0 -e "/opt/ros/kinetic/bin/roslaunch sim_create gmapping.launch"


sleep 5

gnome-terminal --geometry = 80x5+0+0 -e "/opt/ros/kinetic/bin/rosrun sim_create key_teleop.py"


