#! /usr/bin/env python

import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from std_msgs.msg import Float64, Float64MultiArray


class axisToMarker:
    def __init__(self):
        #self.axis_x = rospy.Subscriber("/calced_axis_x", Float64, self.callback)
        self.axis = rospy.Subscriber("/calced_axis", Float64MultiArray, self.callback)
        self.mark_pub = rospy.Publisher("scan_mark", MarkerArray, queue_size=5)
        self.markerArray = MarkerArray()
        self.m_id = 0

    def callback(self, data):
        # print(data.data)
        t_mark = self.put_marker(data.data)
        
        if self.m_id == 360:
            self.mark_pub.publish(self.markerArray)
            self.markerArray = MarkerArray()
            self.m_id = 0
        else:
            if t_mark == -1:
                pass
            else:
                t_mark.id = self.m_id
                self.markerArray.markers.append(t_mark)

        self.m_id += 1

    def put_marker(self, _axis):
        if _axis[0] == 0.0 or _axis[1] == 0.0:
            return -1
        marker = Marker()
        marker.header.frame_id = "/laser"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05
        marker.color.a = 1.0
        marker.color.r = 0
        marker.color.g = 1.0
        marker.color.b = 0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = _axis[0]
        marker.pose.position.y = _axis[1]
        marker.pose.position.z = 0.001
        
        return marker


def run():
    rospy.init_node("get_axis", anonymous=True)
    at = axisToMarker()
    rospy.spin()


if __name__ == "__main__":
    run()
