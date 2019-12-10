#-------------------------------------------------------------------------------
# Name:         25_test_hmgcode
# Description:  
# Author:       凯骏
# Date:         12/5/19
#-------------------------------------------------------------------------------
from hmgcode.HMGcode import HMGcode
import cv2 as cv;
import numpy as np;

# filename = "./assets/svg/girl.gcode"
# filename = "./assets/test/hmcxy.gcode"
# filename = "./assets/test/hmcxy22.gcode"
# filename = "./assets/test/helloworld.gcode"
filename = "./assets/test/hmcxy111.gcode"
# filename = "./assets/test/test3.gcode"

gcode = HMGcode();
gcode.parse(filename)
# 绘制的起始坐标
offsetPos = (300,300)




dst = np.zeros((1080,1920,3),np.uint8);

pre = None

for g in gcode.gcodes:
    if g.cmd_type == "G":
        if g.cmd_value==92:
            print("移动到起始点")
            pre = None
        elif g.cmd_value == 1: # G1
            print("移动到某个点")
            x = g.words[1].value;
            y = g.words[2].value;

            x = int(x + offsetPos[0])
            y = int(-y + offsetPos[1])

            print("移动到某个点:",x,y)
            cur = (x,y)
            if pre is None:
                pre = cur;

            cv.line(dst, pre, cur, (255, 255, 0), 1);
            pre = cur;

            cv.imshow("dst",dst);
            cv.waitKey(10);

    elif g.cmd_type == "M":
        if g.comment == "pen up":
            print("抬起笔",g.comment)
            pre = None;
        elif g.comment == "pen down":
            # 下笔操作
            pass
        elif g.comment == "turn off servo":
            # 绘制完成，要结束啦！
            break;


cv.waitKey(0);