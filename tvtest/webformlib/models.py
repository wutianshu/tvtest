#!/usr/bin/env python
# coding:utf-8
"""锚点对象模型
"""
import json
import logging

from tvtest import db

# 获取日志句柄
logger = logging.getLogger(__name__)


class WebForm(db.Model):
    __tablename__ = 'webform'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    webformKey = db.Column(db.String(64), unique=True, nullable=False)
    webformName = db.Column(db.String(64), nullable=False)
    webformDesc = db.Column(db.String(2048), nullable=True)
    owner = db.Column(db.String(128), nullable=True)
    webformRules = db.Column(db.String(4096), nullable=True)
    webformOption = db.Column(db.String(4096), nullable=True)
    domain = db.Column(db.String(64), nullable=True)
    module = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """将用户对象格式化输出"""
        return str({
            'id': self.id,
            'domain': self.domain,
            'webformKey': self.webformKey,
            'webformName': self.webformName,
            'webformDesc': self.webformDesc,
            'owner': self.owner,
            'webformRules': json.loads(self.webformRules),
            'webformOption': json.loads(self.webformOption),
            'module': self.module
        })

    def to_json(self):
        return {
            'id': self.id,
            'domain': self.domain,
            'webformKey': self.webformKey,
            'webformName': self.webformName,
            'webformDesc': self.webformDesc,
            'owner': self.owner,
            'webformRules': json.loads(self.webformRules),
            'webformOption': json.loads(self.webformOption),
            'module': self.module
        }


class FormFiled(db.Model):
    __tablename__ = 'form_field'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    webformid = db.Column(db.Integer, db.ForeignKey('webform.id'))
    type = db.Column(db.String(64), nullable=False)
    field = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    placeholder = db.Column(db.String(2048))
    value = db.Column(db.String(64))
    required = db.Column(db.String(64))
    optionstext = db.Column(db.String(2048))

    def __repr__(self):
        """将用户对象格式化输出"""
        return str(
            {'id': self.id, 'webformid': self.webformid, 'type': self.type, 'field': self.field,
             'title': self.title, 'placeholder': self.placeholder, 'value': self.value, 'required': self.required,
             'optionstext': self.optionstext}
        )

    def to_json(self):
        return {'id': self.id, 'webformid': self.webformid, 'type': self.type, 'field': self.field,
                'title': self.title, 'placeholder': self.placeholder, 'value': self.value, 'required': self.required,
                'optionstext': self.optionstext}
