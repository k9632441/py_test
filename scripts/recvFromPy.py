#! /usr/bin/env python
# -*-coding:utf-8-*-


import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class img_converter:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/Canny_img", Image, self.callback)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "mono8")
        except CvBridgeError as e:
            print("converting error")
            print(e)


        cv2.imshow("Image window", cv_image)
        cv2.waitKey(1)


def run():
    rospy.init_node('image_receiver', anonymous=True)
    ic = img_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Program down")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
