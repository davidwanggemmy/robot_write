#! /usr/bin/env python
# coding=utf-8

#-------------------------------------------------------------------------------
# Name:         Line
# Description:  单行命令
# Author:       凯骏
# Date:         12/5/19
#-------------------------------------------------------------------------------
import re
from .Word import Word
from .Gcode import Gcode
REGEX_FLOAT = re.compile(r'^\s*-?(\d+\.?\d*|\.\d+)') # testcase: ..tests.test_words.WordValueMatchTests.test_float
REGEX_INT = re.compile(r'^\s*-?\d+')
REGEX_POSITIVEINT = re.compile(r'^\s*\d+')
REGEX_CODE = re.compile(r'^\s*\d+(\.\d)?') # float, but can't be negative

# Value cleaning functions
def _clean_codestr(value):
    if value < 10:
        return "0%g" % value
    return "%g" % value

CLEAN_NONE = lambda v: v
CLEAN_FLOAT = lambda v: "{0:g}".format(round(v, 3))
CLEAN_CODE = _clean_codestr
CLEAN_INT = lambda v: "%g" % v

WORD_MAP = {
    # Descriptions copied from wikipedia:
    #   https://en.wikipedia.org/wiki/G-code#Letter_addresses

    # Rotational Axes
    'A': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Absolute or incremental position of A axis (rotational axis around X axis)",
        'clean_value': CLEAN_FLOAT,
    },
    'B': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Absolute or incremental position of B axis (rotational axis around Y axis)",
        'clean_value': CLEAN_FLOAT,
    },
    'C': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Absolute or incremental position of C axis (rotational axis around Z axis)",
        'clean_value': CLEAN_FLOAT,
    },
    'D': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Defines diameter or radial offset used for cutter compensation. D is used for depth of cut on lathes. It is used for aperture selection and commands on photoplotters.",
        'clean_value': CLEAN_FLOAT,
    },
    # Feed Rates
    'E': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Precision feedrate for threading on lathes",
        'clean_value': CLEAN_FLOAT,
    },
    'F': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Feedrate",
        'clean_value': CLEAN_FLOAT,
    },
    # G-Codes
    'G': {
        'class': float,
        'value_regex': REGEX_CODE,
        'description': "Address for preparatory commands",
        'clean_value': CLEAN_CODE,
    },
    # Tool Offsets
    'H': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Defines tool length offset; Incremental axis corresponding to C axis (e.g., on a turn-mill)",
        'clean_value': CLEAN_FLOAT,
    },
    # Arc radius center coords
    'I': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Defines arc center in X axis for G02 or G03 arc commands. Also used as a parameter within some fixed cycles.",
        'clean_value': CLEAN_FLOAT,
    },
    'J': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Defines arc center in Y axis for G02 or G03 arc commands. Also used as a parameter within some fixed cycles.",
        'clean_value': CLEAN_FLOAT,
    },
    'K': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Defines arc center in Z axis for G02 or G03 arc commands. Also used as a parameter within some fixed cycles, equal to L address.",
        'clean_value': CLEAN_FLOAT,
    },
    # Loop Count
    'L': {
        'class': int,
        'value_regex': REGEX_POSITIVEINT,
        'description': "Fixed cycle loop count; Specification of what register to edit using G10",
        'clean_value': CLEAN_INT,
    },
    # Miscellaneous Function
    'M': {
        'class': float,
        'value_regex': REGEX_CODE,
        'description': "Miscellaneous function",
        'clean_value': CLEAN_CODE,
    },
    # Line Number
    'N': {
        'class': int,
        'value_regex': REGEX_POSITIVEINT,
        'description': "Line (block) number in program; System parameter number to change using G10",
        'clean_value': CLEAN_INT,
    },
    # Program Name
    'O': {
        'class': str,
        'value_regex': re.compile(r'^.+$'), # all the way to the end
        'description': "Program name",
        'clean_value': CLEAN_NONE,
    },
    # Parameter (arbitrary parameter)
    'P': {
        'class': float, # parameter is often an integer, but can be a float
        'value_regex': REGEX_FLOAT,
        'description': "Serves as parameter address for various G and M codes",
        'clean_value': CLEAN_FLOAT,
    },
    # Peck increment
    'Q': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Depth to increase on each peck; Peck increment in canned cycles",
        'clean_value': CLEAN_FLOAT,
    },
    # Arc Radius
    'R': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Defines size of arc radius, or defines retract height in milling canned cycles",
        'clean_value': CLEAN_FLOAT,
    },
    # Spindle speed
    'S': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Defines speed, either spindle speed or surface speed depending on mode",
        'clean_value': CLEAN_FLOAT,
    },
    # Tool Selecton
    'T': {
        'class': str,
        'value_regex': REGEX_POSITIVEINT, # tool string may have leading '0's, but is effectively an index (integer)
        'description': "Tool selection",
        'clean_value': CLEAN_NONE,
    },
    # Incremental axes
    'U': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Incremental axis corresponding to X axis (typically only lathe group A controls) Also defines dwell time on some machines (instead of 'P' or 'X').",
        'clean_value': CLEAN_FLOAT,
    },
    'V': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Incremental axis corresponding to Y axis",
        'clean_value': CLEAN_FLOAT,
    },
    'W': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Incremental axis corresponding to Z axis (typically only lathe group A controls)",
        'clean_value': CLEAN_FLOAT,
    },
    # Linear Axes
    'X': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Absolute or incremental position of X axis.",
        'clean_value': CLEAN_FLOAT,
    },
    'Y': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Absolute or incremental position of Y axis.",
        'clean_value': CLEAN_FLOAT,
    },
    'Z': {
        'class': float,
        'value_regex': REGEX_FLOAT,
        'description': "Absolute or incremental position of Z axis.",
        'clean_value': CLEAN_FLOAT,
    },
}

class Line:

    def __init__(self,cmd_str):

        self.words = None;
        # 切割gcode成 命令 和 注释部分
        line_regex = re.compile(r'^(?P<block_and_comment>.*?)?(?P<macro>%.*%?)?\s*$')

        if cmd_str is not None:
            # 找到命令和备注
            match = line_regex.search(cmd_str);

            block_and_comment = match.group('block_and_comment')
            # 切割命令和备注
            comment_reg = re.compile(r'\((?P<text>[^\)]*)\)')
            # ['G4 P150 ', 'wait 150ms', '']
            match = comment_reg.split(block_and_comment);
            # 命令 'G4 P150 '
            cmd = match[0]
            if len(match)>2:
                # 注释内容 'wait 150ms'  注释也有可能为空
                self.comment = match[1]
            else:
                self.comment = "";
            if cmd is not None and cmd !="":
                # 删除多余的空白
                cmd = re.sub(r'(^\s+|\s+$)', '', cmd)  # remove whitespace padding
                cmd = re.sub(r'\s+', ' ', cmd)

                # print("cmd:%s"%cmd)
                result = self.text2words(cmd);
                # print("result:",result)
                self.words = list(self.text2words(cmd))
                # print("words:", self.words)



    def getGcode(self):
        if self.words is not None:
            return Gcode(self.words,self.comment);
        else:
            return None;


    def text2words(self,cmd):
        """
        :param cmd : gode代码
        """
        next_word = re.compile(r'^.*?(?P<letter>[%s])' % ''.join(WORD_MAP.keys()), re.IGNORECASE)

        index = 0
        while True:
            letter_match = next_word.search(cmd[index:])
            if letter_match:
                # Letter
                letter = letter_match.group('letter').upper()
                index += letter_match.end()  # propogate index to start of value

                # Value
                value_regex = WORD_MAP[letter]['value_regex']
                value_match = value_regex.search(cmd[index:])
                # if value_match is None:
                #     raise GCodeWordStrError("word '%s' value invalid" % letter)
                value = value_match.group()  # matched text

                #print("letter:%s,value:%s"%(letter,value))
                yield Word(letter, WORD_MAP[letter]['class'](value))

                index += value_match.end()  # propogate index to end of value
            else:
                break
