#! /usr/bin/env python
# coding=utf-8

#-------------------------------------------------------------------------------
# Name:         Word
# Description:  每一行gcode代码，由若干个word组成
# Author:       凯骏
# Date:         12/5/19
#-------------------------------------------------------------------------------
class Word:

    def __init__(self,cmd_type,value):
        self.cmd_type = cmd_type;
        self.value= value;


    def __str__(self):
        return "{}:{}".format(self.cmd_type,self.value);

    def __repr__(self):
        return self.__str__();