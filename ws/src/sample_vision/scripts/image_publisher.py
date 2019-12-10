#!/usr/bin/env python
# coding:utf-8

import rospy

from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

cvBridge = CvBridge()


def imageCallback(msg):
    if not isinstance(msg, Image):
        return

    # cv bridge
    # Ros Image -> OpenCv Mat
    mat = cvBridge.imgmsg_to_cv2(msg, "bgr8")
    cv2.imshow("pymat", mat)
    cv2.waitKey(3)

    # OpenCv Mat -> Ros Image
    imgmsg = cvBridge.cv2_to_imgmsg(mat, "bgr8")
    publisher.publish(imgmsg)


if __name__ == '__main__':
    # 创建节点
    nodeName = "image_subscriber"
    rospy.init_node(nodeName)

    pubName = "/haha"
    publisher = rospy.Publisher(pubName, Image, queue_size=1000)

    topicName = "/usb_cam/image_raw"
    rospy.Subscriber(topicName, Image, imageCallback)

    # 阻塞线程
    rospy.spin()
