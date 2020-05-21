# -*- coding: utf-8 -*-


class Handler(object):
    """
    对Parser发起的方法调用进行处理的对象

    Parser将每个文本块传入handler，调用方法start，end，feed使标签补充完整，
    其中包括需要替换（过滤方法sub（））掉文本块中的需要打上标签的文本。
    """

    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method): return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def substitution(match):
            res = self.callback('sub_', name, match)
            if res is None: match.group(0)
            return res

        return substitution



class HTMLRenderer(Handler):
    """
    用于渲染HTML具体程序

    可以通过超类Handler实现调用start(),sub(),end()来访问类方法，实现了HTML文档的具体标记
    """
    def start_document(self , *name):
        print('<!DOCTYPE html>\n<html><head><title>' + name +'</title></head><body>')
    def end_document(self):
        print('</body></html>')
    def start_paragraph(self):
        print('<p>')
    def end_paragraph(self):
        print('</p>')
    def start_heading(self):
        print('<h2>')
    def end_heading(self):
        print('</h2>')
    def start_list(self):
        print('<ul>')
    def end_list(self):
        print('</ul>')
    def start_listitem(self):
        print('<li>')
    def end_listitem(self):
        print('</li>')
    def start_title(self):
        print('<h1>')
    def end_title(self):
        print('</h1>')
    def sub_emphasis(self, match):
        return '<em>{}</em>'.format(match.group(1))
    def sub_url(self , match):
        return '<a href="{}">{}</a>'.format(match.group(1) , match.group(1))
    def sub_mail(self , match):
        return '<a href="mailto:{}">{}</a>'.format(match.group(1) , match.group(1))
    def feed(self , data):
        print(data)
