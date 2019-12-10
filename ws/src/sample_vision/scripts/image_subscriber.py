#!/usr/bin/env python
# coding:utf-8
from tensorflow import keras
import rospy
import matplotlib.pyplot as plt
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from keras.models import load_model
import numpy as np
cvBridge = CvBridge()

def predict(binary):
    print(0)
    classifier = load_model("/home/wang/Downloads/mnist_10_epoch.h5")
    print(1)
    predict = classifier.predict_classes(binary.reshape(1,28,28,1), 1,  batch_size=32,verbose = 0)[0]
    print("预测数字为:{}".format(predict))

def imageCallback(msg):
    if not isinstance(msg, Image):
        return
    # cv bridge
    # Ros Image -> OpenCv Mat
    mat = cvBridge.imgmsg_to_cv2(msg, "bgr8")
    cv2.imshow("pymat", mat)
    cv2.waitKey(3)

    cv2.rectangle(mat, (100,100),(400,400),(255, 0, 0),5)
    cv2.imshow("pyim",mat)
    cv2.waitKey(3)

    croppedImage=mat[100:400,100:400]
    dst=cv2.resize(croppedImage,(28,28))
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))


    gray2 = cv2.erode(gray, element)


    # 使用算子进行降噪
    x = cv2.Sobel(gray2, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(gray2, cv2.CV_16S, 0, 1)
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    # 选择阀值对图片进行二值化处理
    v,binary=cv2.threshold(dst,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    constant = cv2.copyMakeBorder(
        binary, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=0)
    cv2.imshow("binary",constant)
    cv2.waitKey(3)
    predict(binary)




if __name__ == '__main__':
    # 创建节点
    nodeName = "image_subscriber"
    rospy.init_node(nodeName)

    topicName = "/usb_cam/image_raw"
    rospy.Subscriber(topicName, Image, imageCallback)

    # 阻塞线程
    rospy.spin()
