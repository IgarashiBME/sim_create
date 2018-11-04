import rospy
import csv
import os

if __name__ == '__main__':
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
    print waypoints
    print waypoints[1][0]

    for pose in waypoints:
        print pose
