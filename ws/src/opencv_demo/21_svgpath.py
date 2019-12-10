"""
  写字项目：  相机拍照，识别出数字，操作机械臂写出这个字

    1. 相机拍照，获取到手写图片区域 8  libfreeknect.so cpp代码
    2. 截取出手写区域 ：              cpp
    3. 识别数字：pytorch 8                          python代码  8
    4. 获取数字8的路径信息            svg ---->      python   -->8.svg
    5. 根据路径操作机械臂                     aubo官方SDK:  c++，python

    ros


    svg python --> ROS ---> cpp/python操作机械

    机械 写字的 流程 ；
        1. CAD , 雕刻 ---> 字库 ---> gcode
        2. SVG


    准备字库： 0-9  svg   输入文本 --> 解析每个文字，数字，符号 ----》找到对应的svg/gcode ----> 操作机械按照指定的路径运动
        sudo apt-get install inkscape  开源的图像处理软件

        导出： 数字，汉子 的svg
        导出： 简笔画


    从svg中获取路径信息:   移动， 绘制直线 绘制贝塞尔曲线   妇愁者联盟

        1. xml解析
        2. 获取所有path节点
        3. 遍历每一个path获取属性d 对应的信息
        4. 解析d中svg指令

    https://www.jianshu.com/p/0c9b4b681724


"""

import cv2 as cv;
import numpy as np;

# 解析Xml工具
from xml.dom import minidom
# 解析svg的工作 ： 直线  曲线 移动指令
from svg.path import parse_path


# read the SVG file
# doc = minidom.parse('./assets/svg/test0.svg')
# # 大字
# doc = minidom.parse('./assets/svg/da.svg')
# doc = minidom.parse('heimat1.svg')
# # 我爱北京天安门
# doc = minidom.parse('./assets/svg/wabjtam.svg')



# doc = minidom.parse('./assets/svg/ketty2.svg')



# 空心黑马程序员
# doc = minidom.parse('./assets/svg/heima1.svg')
# doc = minidom.parse('drawing.svg')

# # hell ketty
# doc = minidom.parse('./assets/svg/helloKetty.svg')
#
# # 单笔黑马程序员 axisDraw  : CorelDraw ---> 将图像变成单像素  ---> inkscape ----> 获取路径
# doc = minidom.parse('./assets/svg/hmcxy.svg')
doc = minidom.parse('./assets/test/test1.svg')
doc = minidom.parse('./assets/test/test2.svg')
#
# doc = minidom.parse('girl2.svg')
# doc = minidom.parse('girl3.svg')
# doc = minidom.parse('girl4.svg')
# doc = minidom.parse('girl5.svg')
# doc = minidom.parse('girl6.svg')


# doc = minidom.parse('heimazs.svg')
# doc = minidom.parse('drawing.svg')



# doc = minidom.parse('./assets/svg/2.svg')
# doc = minidom.parse('heimat1.svg')
# doc = minidom.parse('./assets/svg/girl7.svg')
# doc = minidom.parse('./assets/svg/0.svg')
# doc = minidom.parse('heimat1.svg')



path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]

# 释放xml文档
doc.unlink()


# 三阶贝塞尔曲线 （x,y）= P1*t^3 + P2*3*t^2*(1-t) + P3*3*t*(1-t)^2 + P4*(1-t)^3  
def BerzierCurve3(u ,p1,p2,p3,p4):
    a = np.power(u,3)*p1;
    b = (3*np.power(u,2)*(1-u))*p2;
    c = (3*u*np.power((1-u),2))*p3;
    d = np.power((1-u),3)*p4;
    r = np.add(np.add(a,b),np.add(c,d))
    return r;



#  二阶贝塞尔曲线公式 点= （1-t）^2 *P1 + 2*t(1-t)*P2 + t^2*P3
def BerzierCurve2(t,p1,p2,p3):
    a = np.power((1-t),2)*p1;
    b = 2*t*(1-t)*p2
    c = np.power(t,2)*p3;

    return np.add(np.add(a,b),c);


dst = np.zeros((1080,1920,3),np.uint8);

pre = (0, 0);
# path_string = "m 128.13548,175.69149 c -0.52041,-4.03103 -1.53238,-8.98698 9,-16.94122 -1.61.509217,-2.53371 0
for path_string in path_strings:
    # 解析svg中的指令  ： move  三阶贝塞尔 二阶贝塞尔 直线
    path = parse_path(path_string)

    for e in path:
        # print(e)
        if type(e).__name__ == "Move":
             # print(e.start.real,"  ",e.start.imag);
             # x0 = e.start.real
             # y0 = e.start.imag
             # x1 = e.end.real
             # y1 = e.end.imag
             # print("(%.2f, %.2f) - (%.2f, %.2f)" % (x0, y0, x1, y1))
             pre = (int(e.start.real),int(e.start.imag));

             cv.line(dst,pre, pre, (255, 0, 0), 1);
             print("移动",pre)

        elif type(e).__name__ == 'CubicBezier':
            print("当前正在绘制三阶贝塞尔")
            # 三阶贝塞尔 曲线
            p1 = np.array([e.start.real,e.start.imag])
            p2 = np.array([e.control1.real,e.control1.imag])
            p3 = np.array([e.control2.real,e.control2.imag])
            p4 = np.array([e.end.real,e.end.imag])

            r = BerzierCurve3(0, p1, p2, p3, p4)
            pre = (int(r[0]),int(r[1]))
            for i in range(1,40):
                u = i/40;
                r = BerzierCurve3(u, p1, p2, p3, p4)
                x = int(r[0])
                y = int(r[1])
                cur=(x,y);

                b = np.random.randint(0, 255)
                g = np.random.randint(0, 255)
                r = np.random.randint(0, 255)
                # cv.waitKey(5)
                cv.imshow("dst", dst);
                cv.line(dst,pre,cur,(b,g,r),1);
                # 保存当前点，为了便于下一次连线
                pre = cur


        elif type(e).__name__ == 'QuadraticBezier':
            print("当前正在绘制二阶贝塞尔曲线")
            # 二阶贝塞尔
            p1 = np.array([e.start.real, e.start.imag])
            p2 = np.array([e.control.real, e.control.imag])
            p3 = np.array([e.end.real, e.end.imag])

            # 绘制起始点
            r = BerzierCurve2(0, p1, p2, p3)
            pre = (int(r[0]), int(r[1]))



            for i in range(1, 40):
                u = i / 40;
                r = BerzierCurve2(u, p1, p2, p3)
                x = int(r[0])
                y = int(r[1])
                cur = (x, y);

                b = np.random.randint(0, 255)
                g = np.random.randint(0, 255)
                r = np.random.randint(0, 255)
                # cv.waitKey(5)
                cv.imshow("dst", dst);
                cv.line(dst, pre, cur, (b, g, r), 1);
                pre = cur


        elif type(e).__name__ == 'Line':
            x0 = e.start.real
            y0 = e.start.imag
            x1 = e.end.real
            y1 = e.end.imag
            print("当前正在绘制直线....(%.2f, %.2f) - (%.2f, %.2f)" % (x0, y0, x1, y1))
            cv.line(dst,(int(x0),int(y0)),(int(x1),int(y1)),(0,0,255),1);
            # pre = (int(x1),int(y1))

        else:
            print("未知的类型....")


        cv.waitKey(5);
        cv.imshow("dst", dst);

print("绘制内容已经完成")
cv.waitKey(0)





