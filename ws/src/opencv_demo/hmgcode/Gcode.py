#-------------------------------------------------------------------------------
# Name:         Gcode
# Description:  Line解析完之后，封装成Gcode对象
# Author:       凯骏
# Date:         12/5/19
#-------------------------------------------------------------------------------
from .Word import Word
class Gcode:

    def __init__(self,words,comment):
        """
        :param words:  命令
        :param comment: 注释
        """
        self.words = words;
        self.cmd_type = words[0].cmd_type; # G
        self.cmd_value = words[0].value;   # 1
        self.comment = comment;

        # print("cmd_type:",self.cmd_type)

    def __str__(self):
        return "type:{},type_value:{},words:{},comment:{}".format(self.cmd_type,self.cmd_value,self.words,self.comment);

    def __repr__(self):
        return self.__str__();