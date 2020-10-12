#! /usr/bin/env python
# -*-coding:utf-8-*-

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class img_converter:
    def __init__(self):
        self.image_pub = rospy.Publisher("image_topic_2", Image, queue_size=5)
        self.canny_pub = rospy.Publisher("Canny_img", Image, queue_size=5)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)

    def callback(self, data):
        # usb_cam으로 받은 이미지를 bridge의 멤버함수 imgmsg_to_cv2를 이용하여 numpy형 객체로 변환
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print("converting error")
            print(e)

        #cv2.imshow("Image window", cv_image)
        #cv2.waitKey(1)

        gray = cv2.Canny(cv_image, 100, 150)

        # 위와 반대 변환 image to imgmsg
        # cv_image = 원본
        # gray = Canny 이미지_canny는 흑백이미지로 mono8
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
            self.canny_pub.publish(self.bridge.cv2_to_imgmsg(gray, "mono8"))
        except CvBridgeError as e:
            print("publish error")
            print(e)



def run():
    rospy.init_node('image_converter', anonymous=True)
    ic = img_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Program down")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
