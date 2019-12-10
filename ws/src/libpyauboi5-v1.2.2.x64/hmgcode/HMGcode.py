#! /usr/bin/env python
# coding=utf-8

#-------------------------------------------------------------------------------
# Name:         HMGode
# Description:  黑马程序员简单易用的Gcode python工具包
# Author:       凯骏
# Date:         12/5/19
#-------------------------------------------------------------------------------
from .Line import Line
class HMGcode:

    def __init__(self):
        print("")
        self.filename = "";
        # 保存所有解析的gcode
        self.gcodes = [];

    def parse(self,filename):
        """
            :param filename: gcode文件名
        """
        self.filename = filename;

        # 打开文件读取文件的每一行代码
        with open(filename, 'r') as fh:
            for line_str in fh.readlines():

                line = Line(line_str)

                gcode = line.getGcode();

                if gcode is not None:
                    self.gcodes.append(gcode);