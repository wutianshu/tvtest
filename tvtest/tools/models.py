#!/usr/bin/env python
# coding:utf-8
"""锚点对象模型
"""
import json
import logging

from tvtest import db

# 获取日志句柄
logger = logging.getLogger(__name__)





class Mock(db.Model):
    __tablename__ = 'mock'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(255))
    head = db.Column(db.String(2048))
    body = db.Column(db.String(4096))
    desc = db.Column(db.String(255))
    owner = db.Column(db.String(255))

    def to_json(self):
        return {'id': self.id, 'key': self.key, 'head': self.head, 'body': self.body, 'desc': self.desc,
                'owner': self.owner}

    def __repr__(self):
        """将用户对象格式化输出"""
        return str(
            {'id': self.id, 'key': self.key, 'head': self.head, 'body': self.body, 'desc': self.desc,
             'owner': self.owner}
        )
