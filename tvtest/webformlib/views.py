#!/usr/bin/env python
# coding:utf-8

import json
import logging
from flask import current_app
from os import environ
from tvtest import db
import requests
import flask
from flask import request, jsonify
from tvtest.webformlib import webformlib
from .models import WebForm, FormFiled

# 自定义日志logger
logger = logging.getLogger(__name__)


@webformlib.route('/deleteWebform', methods=['POST', 'GET'])
def delete_webform():
    key = request.values.get("webformKey")
    webform = WebForm.query.filter_by(webformKey=key).first()
    if not webform:
        return jsonify({"message": "没有查询到该表单"})
    try:
        db.session.delete(webform)
        db.session.commit()
    except:
        return jsonify({"message": "系统异常，删除数据失败", "status": False})
    else:
        return jsonify({"message": "删除成功", "status": True})


@webformlib.route('/saveWebform', methods=['POST', 'GET'])
def save_webform():
    data = request.get_json()
    # logger.info(data)
    webform_key = data['webformkey']
    webform_name = data['webformname']
    webform_desc = data["webformdesc"]
    webform_domain = data['domain']
    webform_module = data['module']
    if data['webformrules']:
        webform_rules = json.dumps(data['webformrules'])
    else:
        webform_rules = '[]'
    webform_option = json.dumps(data['webformoption']) if data['webformoption'] else '{}'

    form = WebForm.query.filter_by(webformKey=webform_key).first()
    if form:
        # 修改数据
        try:
            form.webformName = webform_name
            form.webformDesc = webform_desc
            form.webformRules = webform_rules
            form.webformOption = webform_option
            form.domain = webform_domain
            form.module = webform_module
            db.session.commit()
        except:
            return jsonify({"message": "系统异常，修改数据失败", "status": False})
        else:
            return jsonify({"message": "修改成功，请在表单实验室中查看", "status": True})
    else:
        # 新增数据
        try:
            webform = WebForm(webformKey=webform_key,
                              webformName=webform_name,
                              webformDesc=webform_desc,
                              webformRules=webform_rules,
                              webformOption=webform_option,
                              domain=webform_domain,
                              module=webform_module)
            db.session.add(webform)
            db.session.commit()
        except:
            return jsonify({"message": "系统异常，新增数据失败", "status": False})
        else:
            return jsonify({"message": "保存成功，请在表单实验室中查看", "status": True})


@webformlib.route('/getAllModules', methods=['POST', 'GET'])
def get_all_module():
    modules = db.session.query(WebForm.module).group_by(WebForm.module).all()
    temp = []
    # for m in modules:
    #     results = WebForm.query.filter_by(module=m[0]).all()
    #     rs = []
    #     for r in results:
    #         row = r.to_json()
    #         rs.append(row)
    #     temp.append({m[0]: rs})
    for i in modules:
        temp.append(i[0])
    return jsonify(temp)


@webformlib.route('/getAllWebform', methods=['POST', 'GET'])
def get_all_webform():
    temp = []
    module = request.values.get("module")
    if module:
        results = WebForm.query.filter_by(module=module).all()
        for r in results:
            row = r.to_json()
            temp.append({"key": row["webformKey"], "name": row["webformName"], "module": row["module"]})
        return jsonify(temp)
    results = db.session.query(WebForm).all()
    for r in results:
        row = r.to_json()
        temp.append({"key": row["webformKey"], "name": row["webformName"], "module": row["module"]})
    logger.info(temp)
    return jsonify(temp)


@webformlib.route('/getWebformRules', methods=['POST', 'GET'])
def get_webform_rules():
    key = request.values.get("webformKey")
    st = WebForm.query.filter_by(webformKey=key).all()
    if not st:
        return jsonify({"message": "没有查询到该表单", "status": False, "data": None})
    data = WebForm.query.filter_by(webformKey=key).first().to_json()

    return jsonify({"message": "查询成功", "status": True, "data": data})
