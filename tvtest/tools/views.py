#!/usr/bin/env python
# coding:utf-8

import random, datetime
import difflib
import json
import logging
from flask import current_app
from tvtest.common.exception import *

from flask import request, jsonify, g
from tvtest.tools import tools

from tvtest import db
from .models import Mock

logger = logging.getLogger(__name__)


@tools.route('/test', methods=['GET', 'POST'])
def test():
    data = {'status': 1, 'message': 'success', 'data': 'success'}
    return jsonify(data)


@tools.route('/test400', methods=['GET', 'POST'])
def test400():
    raise ToolException('错误了,返回400')


@tools.route('/test500', methods=['GET', 'POST'])
def test500():
    1 / 0


@tools.route('/setMock', methods=['POST', 'GET'])
def setMock():
    mock_data = request.get_json()  # 字典
    mock_head = mock_data['head']
    mock_body = mock_data['body']
    mock_key = mock_data['key']
    mock_desc = mock_data['desc']
    mock_owner = mock_data['owner']
    print(mock_key, mock_head, mock_body, mock_desc)
    print(type(mock_key), type(mock_head), type(mock_body), type(mock_desc))
    if not mock_key:
        raise PermissionError('KEY值不能为空')
    try:
        json.loads(mock_head)
        json.loads(mock_body)
    except:
        raise PermissionError('保存失败,响应头和响应内容必须是json格式')
    exist = db.session.query(Mock).filter_by(key=mock_key).all()  # 该key是否存在
    if exist:
        data = {"head": mock_head, "body": mock_body, "desc": mock_desc, "owner": mock_owner}
        db.session.query(Mock).filter_by(key=mock_key).update(data)
        try:
            db.session.commit()
        except:
            raise PermissionError('数据库更新失败')
    else:
        m = Mock(key=mock_key,
                 head=mock_head,
                 body=mock_body,
                 desc=mock_desc,
                 owner=mock_owner)
        try:
            db.session.add(m)
            db.session.commit()
        except:
            raise PermissionError('数据库保持失败')
    result = {"data": mock_key, "message": "设置成功", "status": 0}
    return jsonify(result)


@tools.route('/getMock', methods=['POST', 'GET'])
def getMock():
    key = request.values.get('key')
    exist = db.session.query(Mock).filter_by(key=key).all()  # 该key是否存在
    if not exist:
        result = {"data": "", "message": "缓存中无mock的key值", "status": -1}
        return jsonify(result)
    mock_info = db.session.query(Mock).filter_by(key=key).first()
    mock_head = mock_info.head
    mock_body = mock_info.body

    header = json.loads(mock_head)
    return current_app.response_class(mock_body, mimetype='application/json', headers=header)


@tools.route('/queryMock', methods=['POST', 'GET'])
def queryMock():
    data = db.session.query(Mock).all()
    r = []
    for d in data:
        r.append({'key': d.key, 'head': d.head, 'body': d.body, 'desc': d.desc})
    result = {"data": r, "message": "", "status": 0}
    return jsonify(result)
