#! /usr/bin/env python

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan, PointCloud
from geometry_msgs.msg import Point32
from std_msgs.msg import Float64


class rpScanRecever:
    def __init__(self):
        self.lscan = rospy.Subscriber("/scan", LaserScan, self.callback)
        self.pc_pub = rospy.Publisher("/PointCloud", PointCloud, queue_size=5)

    def callback(self, data):
        min_angle = data.angle_min
        min_range = data.range_min
        max_range = data.range_max
        angle_increment = data.angle_increment
        PC_data = PointCloud()
        PC_data.header = data.header
        # PC_data.points.append(Point32(0, 0, 1))
        for i in range(len(data.ranges)):
            x, y = calc_axis_xy(min_angle + angle_increment * i, data.ranges[i], min_range, max_range)
            if [x, y] != [0, 0]:
                PC_data.points.append(Point32(x, y, 1))
        self.pc_pub.publish(PC_data)


def calc_axis_xy(_theta, _distance, _min_range, _max_range):
    if _min_range <= _distance <= _max_range:
        x = np.cos(_theta) * _distance
        y = np.sin(_theta) * _distance
        return (x, y)
    else:
        return (0, 0)

def calc_distance_two_points(_p1, _p2):
    temp1 = _p2[0] - _p1[0]
    temp2 = _p2[1] - _p1[1]

    _d = abs(np.sqrt(float(temp1 * temp1) + float(temp2 * temp2)))
    
    return _d


def calc_cluster(_pcl, maxDistance = 0.2, relatedObject = 5):
    flag = 0
    _object = 0
    object_array = []
    temp = []
    for i in range(1, len(_pcl)-1):
        d = calc_distance_two_points(_pcl[i-1], _pcl[i])
        if d > 0.0001 and d < maxDistance:
            flag += 1
        else:
            if flag > relatedObject:
                _object += 1
            flag = 0

    return _object


def run():
    rospy.init_node('scan_py_receiver', anonymous=True)
    lc = rpScanRecever()
    rospy.spin()
    

if __name__ == "__main__":
    run()
