#include <iostream>
#include "ros/ros.h"

#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "sensor_msgs/Image.h"

using namespace std;

ros::Publisher *publisher = nullptr;
uint seq = 0;

void imageCallback(const sensor_msgs::Image::ConstPtr &msg) {
  //ros 图像数据格式
//  sensor_msgs::Image --> cv::Mat

  const cv_bridge::CvImageConstPtr &ptr = cv_bridge::toCvShare(msg, "bgr8");
  cv::Mat mat = ptr->image;

  cv::imshow("mat", mat);
  cv::waitKey(3);

  // cv::Mat --> sensor_msgs::Image -> 传输出去
  cv_bridge::CvImage image;
//  image.data = cv_bridge::
  image.header.stamp = ros::Time::now();
  image.header.seq = ++seq;
  image.encoding = "bgr8";
  image.image = mat;
  publisher->publish(image.toImageMsg());
}

int main(int argc, char **argv) {
  //初始化节点
  string nodeName = "image_subscriber";
  ros::init(argc, argv, nodeName);
  //创建节点
  ros::NodeHandle node;

  string pubName = "/hello";
  ros::Publisher pub = node.advertise<sensor_msgs::Image>(pubName, 1000);
  publisher = &pub;

  string topicName = "/usb_cam/image_raw";
  ros::Subscriber subscriber = node.subscribe(topicName, 1000, imageCallback);


  //阻塞
  ros::spin();
  return 0;
}