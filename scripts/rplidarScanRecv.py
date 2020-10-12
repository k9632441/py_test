#! /usr/bin/env python

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64, Float64MultiArray


class rpScanRecever:
    def __init__(self):
        self.lscan = rospy.Subscriber("/scan", LaserScan, self.callback)
        self.scan_pub_x = rospy.Publisher("/calced_axis_x", Float64, queue_size=5)
        self.scan_pub_y = rospy.Publisher("/calced_axis_y", Float64, queue_size=5)
        self.scan_pub = rospy.Publisher("/calced_axis", Float64MultiArray, queue_size=5)

    def callback(self, data):
        axis = []
        axis_x = []
        axis_y = []
        min_angle = -3.12313907051
        offset = 0.0174532923847
        for i in range(len(data.ranges)):
            x, y = calc_axis_xy(min_angle + offset * i, data.ranges[i])
            self.scan_pub.publish(data=[x, y])


def calc_axis_xy(_theta, _distance):
    if abs(_distance) == np.inf:
        return (0, 0)
    x = np.cos(_theta) * _distance
    y = np.sin(_theta) * _distance
    return (x, y)


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
