# -*- coding: utf-8 -*-



class Rule(object):
    """
    抽象出所有规则所使用的统一方法，即规则的基类
    """
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True


class HeadingRule(Rule):
    """
    标题只包含一行，不超过70个字符且不以冒号为结尾
    """
    type = 'heading'
    def condition(self, block):
        return '\n' not in block and len(block) <= 70 and not block[-1] == ':'


class TitleRule(Rule):
    type = 'title'
    first = True
    def condition(self, block):
        if not self.first: return False
        self.first = False
        return HeadingRule.condition(self, block)


class ListItemRule(Rule):
    """
    列表项是以连字符打头的段落，在设置格式的过程中，把连字符删除
    """
    type = 'listitem'
    def condition(self, block):
        return block[0] == '-'  # 列表项在文本中的特征可能不相同
    def action(self, block , handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True


class ListRule(ListItemRule):
    """
    列表以紧跟在非列表项文本块后面的列表项打头，以相连的最后一个列表项结束
    """
    type = 'list'
    inside = False  # 判断是否在列表内
    def condition(self, block):
        return True
    def action(self , block , handler):
        if not self.inside and ListItemRule.condition(self , block):
            handler.start(self.type)
            self.type = True
        elif self.inside and not ListItemRule.condition(self , block):
            handler.end(self.type)
            self.type = False
        return False


class ParagraphRule(Rule):
    type = 'paragraph'
    def condition(self , block):
        return True

