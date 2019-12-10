#! /usr/bin/env python
# coding=utf-8

"""
    1.连接机械臂
    2.机械臂初始化 （设置一些速度）
    3. movel, movej
"""
from hmgcode.HMGcode import HMGcode
import numpy as np;
from lib.robotcontrol import *

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

# 定义机械臂开始画画的起始位置
defaultPos = [0.52,-0.13,0.043]

# 定义默认姿态
defaultRPY = [180,0,90]

# 定义机械臂悬停时的初始坐标
initPos = [defaultPos[0],defaultPos[1],defaultPos[2]+0.1]

# 当前z方向的偏移量
offsetZ=0;

# 将像素单位转成米   90dpi   90像素 = 1 英寸 = 2.54厘米    2.54厘米/90像素/100(厘米转米)
# 100,200   单位转成米
def piexl2meter(pos):
    ratio = 2.54/9000
    pos = [-pos[0] * ratio+ defaultPos[0], pos[1]*ratio + defaultPos[1], pos[2]*ratio + defaultPos[2]];
    print("new pos:",pos)
    return pos;

# 移动到目标点
def move2pos(pos):
    global offsetZ
    if len(pos)<3:
        pos.append(offsetZ);
    else:
        offsetZ = pos[2]
    logger.info("pixel:{0}".format(pos));
    pos = piexl2meter(pos);
    logger.info("move2pos:{0}".format(pos))
    # 机械臂移动的单位是米
    robot.move_to_target_in_cartesian(pos, defaultRPY);




try:
    # 链接服务器
    ip = '192.168.36.25'
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

        # 机械臂刚启动，移动到起始位置
        robot.move_to_target_in_cartesian(initPos, defaultRPY);

        # 移动机械臂
        #filename = "./assets/hmcxy.gcode"
        filename = "./assets/helloword.gcode"

        # 解析gcode
        gcode = HMGcode();
        gcode.parse(filename)
        # 初始坐标
        offsetPos = (0, 0)


        pre = None
        for g in gcode.gcodes:
            if g.cmd_type == "G":
                if g.cmd_value == 92:
                    print("移动到起始点")
                    pre = initPos
                elif g.cmd_value == 1:
                    print("移动到某个点")
                    x = g.words[1].value;
                    y = g.words[2].value;

                    x = int(x + offsetPos[0])
                    y = int(-y + offsetPos[1])

                    print("移动到某个点:", x, y)
                    cur = [x, y]
                    # if pre is None:
                    #     pre = cur;

                    move2pos(cur)
                    # cv.line(dst, pre, cur, (255, 255, 0), 1);
                    pre = cur;

                    # cv.imshow("dst", dst);
                    # cv.waitKey(10);

            elif g.cmd_type == "M":
                if g.comment == "pen up":
                    # 抬起笔
                    move2pos([pre[0],pre[1],80])
                    pre = None;
                elif g.comment == "pen down":
                    # 下笔操作
                    move2pos([pre[0],pre[1],0])
                elif g.comment == "turn off servo":
                    # 绘制完成，要结束啦！
                    break;

        # 绘制完成，机械臂回到起始位置
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
    Auboi5Robot.uninitialize()



