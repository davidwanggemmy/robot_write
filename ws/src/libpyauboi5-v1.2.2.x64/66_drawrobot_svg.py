#! /usr/bin/env python
# coding=utf-8

"""
    1.连接机械臂
    2.机械臂初始化 （设置一些速度）
    3. movel, movej
"""



import numpy as np;
from lib.robotcontrol import *


from svg.path import parse_path
from xml.dom import minidom

import rospy
from std_msgs.msg import String
# read the SVG file

# # 大字
# doc = minidom.parse('./svg/1.svg')
# doc = minidom.parse('./svg/2.svg')
# doc = minidom.parse('./svg/da.svg')
# doc = minidom.parse('./svg/heimat1.svg')
# # 我爱北京天安门
# doc = minidom.parse('./assets/svg/wabjtam.svg')


# 将像素单位转成米   90dpi   90像素 = 1 英寸 = 2.54厘米    2.54厘米/100(厘米转米)/90像素   米/像素*像素----》 米
# 100,200   单位转成米
def piexl2meter(pos):
    ratio = 2.54/9000
    pos = [-pos[0] * ratio+ defaultPos[0], pos[1]*ratio + defaultPos[1], pos[2]*ratio + defaultPos[2]];
    print("new pos:",pos)
    return pos;

# 移动到目标点
def move2pos(pos):
    """
    :param pos: 传入进来的数据是以像素为单位的数据
    :return:
    """
    if len(pos)<3:
        pos.append(0);
    logger.info("pixel:{0}".format(pos));
    # 将像素单位的数据转换成以米为单位的数据
    pos = piexl2meter(pos);
    logger.info("move2pos:{0}".format(pos))
    # 机械臂移动的单位是米
    robot.move_to_target_in_cartesian(pos, defaultRPY);

def todo():

    try:
        # 链接服务器
        ip = '192.168.36.28'
        # ip = '192.168.17.250'
        port = 8899
        result = robot.connect(ip, port)

        if result != RobotErrorType.RobotError_SUCC:
            logger.info("connect server{0}:{1} failed.".format(ip, port))
        else:

            # 设置速度
            # robot.set_joint_maxacc([2, 2, 2, 2, 2.5,2])
            # robot.set_joint_maxvelc([2, 2, 2, 2, 2.5,2])

            robot.set_joint_maxacc((1.5, 1.5, 1.5, 1.5, 1.5, 1.5))
            robot.set_joint_maxvelc((1.5, 1.5, 1.5, 1.5, 1.5, 1.5))

            robot.set_end_max_line_acc(0.5)
            robot.set_end_max_angle_acc(0.2)


            robot.move_to_target_in_cartesian(initPos, defaultRPY);


            pre = (0, 0);
            # print the line draw commands
            for path_string in path_strings:

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
                        pre = np.array([e.start.real, e.start.imag]);

                        logger.error("current Type:Move")
                        move2pos([e.start.real, e.start.imag,80]);
                        # 将像素坐标换算成米
                        # print(",m：",pre/7000);
                        # cv.line(dst, pre, pre, (255, 0, 0), 1);

                    elif type(e).__name__ == 'CubicBezier':
                        p1 = np.array([e.start.real, e.start.imag])
                        p2 = np.array([e.control1.real, e.control1.imag])
                        p3 = np.array([e.control2.real, e.control2.imag])
                        p4 = np.array([e.end.real, e.end.imag])

                        r = BerzierCurve3(0, p1, p2, p3, p4)
                        pre = [r[0], r[1]]



                        logger.error("current Type:CubicBezier")
                        # 移动到曲线的起始位置
                        move2pos([r[0], r[1],80]);

                        for i in range(0, 40,3):
                            u = float(i) / 40;
                            r = BerzierCurve3(u, p1, p2, p3, p4)

                            cur = [r[0], r[1]];


                            # 移动机械臂
                            move2pos(cur)
                            pre = cur

                        # 抬起笔
                        move2pos([pre[0], pre[1], 80]);

                    elif type(e).__name__ == 'QuadraticBezier':
                        p1 = np.array([e.start.real, e.start.imag])
                        p2 = np.array([e.control.real, e.control.imag])
                        p3 = np.array([e.end.real, e.end.imag])

                        # r = BerzierCurve2(0, p1, p2, p3)
                        pre = (p1[0], p1[1])

                        # 移动机械臂
                        logger.error("current Type:QuadraticBezier")

                        for i in range(0, 40,10):
                            u = i / 40;
                            r = BerzierCurve2(u, p1, p2, p3)
                            x = r[0]
                            y = r[1]
                            cur = [x, y];

                            # b = np.random.randint(0, 255)
                            # g = np.random.randint(0, 255)
                            # r = np.random.randint(0, 255)
                            # # cv.waitKey(5)
                            # # cv.imshow("dst", dst);
                            # cv.line(dst, pre, cur, (b, g, r), 1);
                            # 移动机械臂
                            move2pos(cur)
                            pre = cur


                    elif type(e).__name__ == 'Line':
                        x0 = e.start.real
                        y0 = e.start.imag
                        x1 = e.end.real
                        y1 = e.end.imag
                        print("(%.2f, %.2f) - (%.2f, %.2f)" % (x0, y0, x1, y1))
                        # cv.line(dst, (int(x0), int(y0)), (int(x1), int(y1)), (0, 0, 255), 1);

                        # 移动机械臂
                        logger.error("current Type:Line")
                        move2pos([x0,y0])
                        move2pos([x1,y1])
                        # 保存上一次的点
                        pre = (int(x1), int(y1))
                        # pre = np.array([x1,y1]);



                    # cv.waitKey(5);
                    # cv.imshow("dst", dst);

            # 将机械臂移动到初始位置
            robot.move_to_target_in_cartesian(initPos, defaultRPY);

            # 断开服务器链接
            robot.disconnect()

    except Exception as e:
        logger.error("robot Event:{0}".format(e))

    finally:
        # 断开服务器链接
        if robot.connected:
            # 断开机械臂链接
            robot.disconnect()
        # 释放库资源
        # Auboi5Robot.uninitialize()







# doc = minidom.parse('./svg/ketty2.svg')



# 空心黑马程序员 可以使用
# doc = minidom.parse('drawing.svg')

# # hell ketty
# doc = minidom.parse('./assets/svg/helloKetty.svg')
#
# # 单笔黑马程序员
# # doc = minidom.parse('./assets/svg/hmcxy.svg')
#
# doc = minidom.parse('girl2.svg')
# doc = minidom.parse('girl3.svg')
# doc = minidom.parse('./svg/da.svg')
# doc = minidom.parse('./svg/2.svg')
# doc = minidom.parse('girl5.svg')
# doc = minidom.parse('girl6.svg')


# doc = minidom.parse('heimazs.svg')
# doc = minidom.parse('drawing.svg')

doc=' '
path_strings=' '

def topicCallback(msg):
    global doc,path_strings
    print msg.data
    # path = '/home/wang/Desktop/0to9/' + msg.data + '.svg'
    path = '/home/wang/Desktop/0to9/'+msg.data+'.svg'
    print path
    doc = minidom.parse(path)
    path_strings = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')]

    doc.unlink()
    print path_strings

    todo()
    # print msg




# 三 P1*t^3 + P2*3*t^2*(1-t) + P3*3*t*(1-t)^2 + P4*(1-t)^3 = Pnew 
def BerzierCurve3(u ,p1,p2,p3,p4):
    a = np.power(u,3)*p1;
    b = (3*np.power(u,2)*(1-u))*p2;
    c = (3*u*np.power((1-u),2))*p3;
    d = np.power((1-u),3)*p4;
    r = np.add(np.add(a,b),np.add(c,d))
    return r;


# 二阶贝塞尔曲线
# 公式 点= （1-t）^2 *P1 + 2*t(1-t)*P2 + t^2*P3
def BerzierCurve2(t,p1,p2,p3):
    a = np.power((1-t),2)*p1;
    b = 2*t*(1-t)*p2
    c = np.power(t,2)*p3;

    return np.add(np.add(a,b),c);


# dst = np.zeros((1080,1920,3),np.uint8);



# 机器人初始化操作
# 初始化logger
logger_init()

# 启动测试
logger.info("{0} test beginning...".format(Auboi5Robot.get_local_time()))

# 系统初始化
Auboi5Robot.initialize()

# 创建机械臂控制类
robot = Auboi5Robot()

# 创建上下文
handle = robot.create_context()



# 打印上下文
logger.info("robot.rshd={0}".format(handle))

# 定义机械臂开始画画的起始位置 单位是米
# 切记单位不要搞错啦！  否则可能撞坏笔头
defaultPos = [0.13,-0.42,-0.06]

# 定义默认姿态
defaultRPY = [180,0,90]

# 定义机械臂悬停时的初始坐标
initPos = [defaultPos[0],defaultPos[1],defaultPos[2]+0.1]

nodeName="subscriber2"
topicName="haha"
rospy.init_node(nodeName)
rospy.Subscriber(topicName,String,topicCallback)
rospy.spin()







