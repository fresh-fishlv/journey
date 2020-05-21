# -*- coding: utf-8 -*-
import sys , re
from handlers import *
from util import *
from rules import *


class Parser(object):
    """
    Parser读取文本文件，应用规则处理文本并且控制整个程序流程
    定义了整个子类的基本流程
    """
    def __init__(self , handlers):
        self.handler = handlers
        self.rules = []
        self.filters = []

    def addRule(self , rule):
        self.rules.append(rule)

    def addFilter(self , pat , name):
        def block_filter(block , Handler):
            return re.sub(pat , Handler.sub(name) , block)
        self.filters.append(block_filter)

    def parse(self , file):
        self.handler.start('document')
        for block in blocks(file):
            for Filter in self.filters:
                block = Filter(block , self.handler)
                for rule in self.rules:
                    if rule.condition(block):
                        last = rule.action(block , self.handler)   # last用来判断这个文本块是否还符合其他规则
                        if last : break
        self.handler.end('document')


class BasicTextParser(Parser):
    def __init__(self , handlers):
        Parser.__init__(self , handlers)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addRule(r'\*(.+?)\*' , 'emphasis')
        self.addRule(r'([a-zA-z]+://[\S]*)' , 'url')
        self.addRule(r'([\S]@[\w]+.[\w]+)' , 'mail')


handler = HTMLRenderer()
parser = BasicTextParser(handler)

parser.parse(sys.stdin)
