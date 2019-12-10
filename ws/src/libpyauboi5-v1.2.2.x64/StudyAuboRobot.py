#! /usr/bin/env python
# coding=utf-8
from lib.robotcontrol import *



def test_rsm():
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

    try:

        # 链接服务器
        ip = '192.168.36.150'
        port = 8899
        result = robot.connect(ip, port)

        if result != RobotErrorType.RobotError_SUCC:
            logger.info("connect server{0}:{1} failed.".format(ip, port))
        else:

            # robot.move_pause()

            joint_radian = (pi/2, 0, pi/4,0, 0, 0)
            # 轴动到初始位置
            robot.move_joint(joint_radian)

            joint_radian = (pi/2, 0, -pi / 4, 0, 0, 0)
            # 轴动到初始位置
            robot.move_joint(joint_radian)

            pos = (0.0, 0.0, 0.0)

            ori = (1.0, 0.0, 0.0, 0.0)

            # # 逆解
            # joint_radian = (
            # 0.39332062005996704, 1.0142878293991089, -1.8255853652954102, -1.2690789699554443, -1.5707889795303345,
            # 0.36539429426193237)
            #
            # robot.move_joint(joint_radian)
            #
            # 获取当前位置
            current_pos = robot.get_current_waypoint()

            logger.info("current_pos={0}".format(current_pos))
            #
            # rpy = (180.0/ 180.0 * pi, 0.0/ 180.0 * pi, 93.448924084472651/ 180.0 * pi)
            # pos = (-0.47550315922145057, -0.28381937141504375, -0.13900255408783696)
            #
            # ori = robot.rpy_to_quaternion(rpy)
            # logger.info("dest ori={0}".format(ori))
            #
            # ik_result = robot.inverse_kin(joint_radian, pos, ori)
            # logger.info(ik_result)
            #
            # robot.move_joint(ik_result['joint'])






            # joint_radian = (
            #     0.31687501072883606, 0.3967222273349762, -1.9043120145797729,
            #     -0.73023837804794312, -1.57082200050354, 3.3982810974121094)

            # joint_radian = ( 0.31687501072883606, 0,0,0,0,0)
            #
            # robot.move_joint(joint_radian)


            # rpy = (180.0 / 180.0 * pi, 0.0 / 180.0 * pi, -90 / 180.0 * pi)
            # pos = (-0.555349, -0.181059, 0.1300)
            #
            # ori = robot.rpy_to_quaternion(rpy)
            # logger.info("dest ori={0}".format(ori))
            #
            # ik_result = robot.inverse_kin(joint_radian, pos, ori)
            # logger.info(ik_result)
            #
            # robot.move_joint(ik_result['joint'])
            #




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

if __name__ == '__main__':
    test_rsm();
