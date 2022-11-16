#!/usr/bin/env python
# coding:utf-8


class TVException(Exception):
    def __init__(self, message, node=None):
        self.status = False
        self.node = node
        self.message = message

    def __str__(self):
        return '状态：{0}，节点：{1}，错误信息：{2}'.format(self.status, self.node, self.message)

    def to_dict(self):
        return {'status': self.status,
                'message': self.message}



class AuthException(TVException):
    pass


class ToolException(TVException):
    pass


class StatisException(TVException):
    pass


class WebFormException(TVException):
    pass
