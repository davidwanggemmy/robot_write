"""
    svg文件的解析

    https://www.jianshu.com/p/0c9b4b681724

    1.svg ---> xml格式的文件

    2.解析xml文件
        path标签
            d属性：包含了当前路径的所有指令

    3.解析输出： 移动指令，直线指令，二阶贝塞尔曲线，三阶贝塞尔曲线

    4. 使用opencv将对应的指令绘制出来
"""

import cv2 as cv;
import numpy as np;

# 解析Xml工具
from xml.dom import minidom
# 解析svg的工作 ： 直线  曲线 移动指令
from svg.path import parse_path


# 读取svg文件
# doc = minidom.parse('./assets/test/test2.svg')
# doc = minidom.parse('./assets/test/test3.svg')
# doc = minidom.parse('./assets/test/apple.svg')
doc = minidom.parse('./assets/test/apple_singleline.svg')
#doc = minidom.parse('./assets/svg/1.svg')
#doc = minidom.parse('./assets/svg/2.svg')
# 加载svg xml格式的文件
#doc = minidom.parse('./assets/test/8_1.svg')
# doc = minidom.parse('./assets/test/dlam.svg')


# 获取节点的信息 ["m 231.75538,163.02425 68.94963,0","m 231.75538,163.02425 68.94963,0"]
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

# 定义空白的页面
dst = np.zeros((1080,1920,3),np.uint8);

pre = (0, 0);
# path_string = "m 128.13548,175.69149 c -0.52041,-4.03103 -1.53238,-8.98698 9,-16.94122 -1.61.509217,-2.53371 0
# 解析每一个d属性对应的value值
for path_string in path_strings:
    # 解析svg中的指令  ： move  三阶贝塞尔 二阶贝塞尔 直线
    path = parse_path(path_string)

    for e in path:

        if type(e).__name__ == "Move":
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

                #

                cv.line(dst,pre,cur,(b,g,r),1);
                cv.imshow("dst", dst);
                # cv.waitKey(50)
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


            # 进行插补
            for i in range(1, 40):
                u = i / 40;
                r = BerzierCurve2(u, p1, p2, p3)
                x = int(r[0])
                y = int(r[1])
                # 当前插补出来的点
                cur = (x, y);

                b = np.random.randint(0, 255)
                g = np.random.randint(0, 255)
                r = np.random.randint(0, 255)
                #cv.waitKey(50)
                cv.imshow("dst", dst);
                # 和前一个点进行直线相连
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
            #cv.waitKey(500)
            cv.imshow("dst", dst);

        else:
            print("未知的类型....")

        cv.waitKey(5);
        cv.imshow("dst", dst);

print("绘制内容已经完成")
cv.waitKey(0)





