#include <iostream>
#include "ros/ros.h"

#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "sensor_msgs/Image.h"

#include "pt_model.h"
#include "pt_tensor.h"
#include<thread>
using namespace std;
using namespace cv;
#include "std_msgs/String.h"

const ros::Publisher* publisher=nullptr ;



void predict(cv::Mat &srcImage) {
    int c;
    int num;
//  Mat srcImage;
//  //预测之前，图片需要转化成28*28的灰度图片， 黑底白字
//  const char *srcImageName = "../../sample/test2.png";
//  srcImage = imread( srcImageName ,CV_8U);

  //模型文件用python的keras可以训练，具体方法见上课视频。
  auto model = pt::Model::create("/home/wang/Downloads/ws/src/sample_vision/model/mnist.model");
//  auto model = pt::Model::create("model/mnist.model");
  pt::Tensor in(28, 28, 1);

  //数据归一化
  float *raw = new float[28 * 28 * 1];
  for (int j = 0; j < 28; j++) {
    uchar *data = srcImage.ptr<uchar>(j);
    for (int i = 0; i < 28; i++) {
      raw[j * 28 + i] = (255.0 - data[i]) / 255.0;
    }
  }

  pt::Tensor::DataVector rawInput(28 * 28);
  for (size_t i = 0; i < 28 * 28; i++) {
    rawInput[i] = (raw[i]);
  }
  in.setData(rawInput);

  // 预测
  pt::Tensor out;
  bool success = model->predict(std::move(in), out);
  // REQUIRE(success);

  //找出最大的概率和所在的位置
  int i = 0;
  float max = 0;
  int index = 0;
  for (; i < out.getData().size(); i++) {
    if (max < out.getData().data()[i]) {
      max = out.getData().data()[i];
      index = i;
    }
  }
    c=cvWaitKey(10);
  if(c=='s') {
      cout << "概率分布:" << out << endl;
      cout << "预测的数字是:" << index << endl;
      cout << "预测的概率是:" << max << endl;
    std_msgs::String ss;
      ss.data = to_string(index);
      publisher->publish(ss);
  }



}



void imageCallback(const sensor_msgs::Image::ConstPtr &msg) {
  //ros 图像数据格式
//  sensor_msgs::Image --> cv::Mat

  const cv_bridge::CvImageConstPtr &ptr = cv_bridge::toCvShare(msg, "bgr8");
  cv::Mat mat = ptr->image;

  cv::imshow("mat", mat);
  cv::waitKey(3);

  // mat -> 识别操作
  //画矩形
  cv::Rect rect(100, 100, 300, 300);
  cv::rectangle(
      mat,
      rect,
      cv::Scalar(255, 0, 0),
      5
  );
  cv::imshow("im", mat);

  cv::waitKey(3);

  //裁剪
  cv::Mat croppedImage = mat(rect);
  cv::Mat dstMat;
  cv::resize(croppedImage, dstMat, Size(28, 28));
  cv::cvtColor(dstMat, dstMat, cv::COLOR_BGR2GRAY);
  Mat kernal=getStructuringElement(MORPH_RECT,Size(3,3));
  Mat dst;
  morphologyEx(dstMat,dst,MORPH_OPEN,kernal);

  cv::Mat binary;
  cv::threshold(dst, binary, 0, 255, CV_THRESH_OTSU + CV_THRESH_BINARY);

  cv::imshow("binary", binary);
  cv::waitKey(3);

  predict(binary);
}

int main(int argc, char **argv) {
  //初始化节点
  string nodeName = "image_subscriber";
  ros::init(argc, argv, nodeName);
  //创建节点
  ros::NodeHandle node;

  string topicName = "/usb_cam/image_raw";
  ros::Subscriber subscriber = node.subscribe(topicName, 1000, imageCallback);

  string nodename2 = "publisher2";
  string topic2Name="haha";
  ros::init(argc, argv, nodename2);
  ros::NodeHandle node2;
  const ros::Publisher &publ = node.advertise<std_msgs::String>(topic2Name, 1000);
    publisher=&publ;

  //阻塞
  ros::spin();
  return 0;
}