import cv2 as cv;
import numpy as np;

"""
  我要用机械臂写字？
    1. 图像平面上 行列表示点 --->  平移到图片正中间坐标系 （cx,cy）
  
"""

src = cv.imread("./assets/heima.png",cv.IMREAD_COLOR);
# src = cv.imread("./assets/hei.png",cv.IMREAD_COLOR);
# src = cv.imread("./assets/logo.png",cv.IMREAD_COLOR);
# 转成灰度图片
gray = cv.cvtColor(src,cv.COLOR_BGR2GRAY);
# 转成二值画 0,255
_,binary = cv.threshold(gray,100,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU);

cv.imshow("binary",binary);
# 获取它的轮廓
_,contours,hierchy = cv.findContours(binary,cv.RETR_CCOMP,cv.CHAIN_APPROX_SIMPLE);

# print(contours);

# cv.drawContours(src,contours,-1,(0,0,255),2);


# 遍历所有轮廓
for c in contours:
    # 遍历每个轮廓中的每一个点
    b = np.random.randint(0, 255)
    g = np.random.randint(0, 255)
    r = np.random.randint(0, 255)
    # 从每一个轮廓中获取每一个点坐标
    for p in c:
        print(p[0]);
        # 绘制一个小圆点
        cv.circle(src,(p[0][0],p[0][1]),1,(b,g,r),2);
        cv.waitKey(50);
        # 刷新图片
        cv.imshow("src", src);

    # 停一秒
    cv.waitKey(1000);
#
#
#

cv.waitKey(0);
