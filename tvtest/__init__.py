#!/usr/bin/env python
# coding=utf-8

import json
import flask
from flask import request, current_app
import logging
import platform

from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound
from tvtest.common.exception import TVException

from tvtest.config import config
from tvtest.log import console, log_handler, err_handler, env

PYTHON_VERSION = platform.python_version()
print('{0}当前python版本：{1}'.format('=' * 8, PYTHON_VERSION))

# 获取日志操作句柄
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# 添加日志采集器
logger.addHandler(console)
if env == 'production':
    logger.addHandler(log_handler)
    logger.addHandler(err_handler)

db = SQLAlchemy()
scheduler = APScheduler()


def create_app(env):
    """工厂函数, 返回app程序对象"""
    app = flask.Flask(__name__)

    # 指定的配置不存在时的默认加载方案
    if env not in iter(list(config.keys())):
        env = 'default'

    # 将配置读取到flask对象中
    app.config.from_object(config[env])
    config[env].init_app(app)

    logger.info('成功加载配置：{}'.format(config[env]))

    scheduler.init_app(app)
    scheduler.start()

    # 数据库
    db.app = app
    db.init_app(app)

    # 调试开关
    disable_exception = app.config.get('EXCEPTION')

    # 注册蓝图

    # 统计模块
    if app.config.get('STATIS'):
        try:
            from tvtest.statis import statis
            app.register_blueprint(statis, url_prefix='/api/statis')
        except disable_exception as e:
            logger.error('{0}启动【statis】模块失败，跳过！{0}'.format('×' * 15))
            logger.exception(e)
        else:
            logger.info('{0}【statis】模块启动成功{0}'.format('√' * 15))

    # 权限模块
    if app.config.get('AUTH'):
        try:
            from tvtest.auth import auth
            app.register_blueprint(auth, url_prefix='/api/auth')
        except disable_exception as e:
            logger.error('{0}启动【auth】模块失败，跳过！{0}'.format('×' * 15))
            logger.exception(e)
        else:
            logger.info('{0}【auth】模块启动成功{0}'.format('√' * 15))

    # 工具模块
    if app.config.get('TOOLS'):
        try:
            from tvtest.tools import tools
            app.register_blueprint(tools, url_prefix='/api/tools')
        except disable_exception as e:
            logger.error('{0}启动【tools】模块失败，跳过！{0}'.format('×' * 15))
            logger.exception(e)
        else:
            logger.info('{0}【tools】模块启动成功{0}'.format('√' * 15))

    # 表单实验室
    if app.config.get('WEBFORMLIB'):
        try:
            from tvtest.webformlib import webformlib
            app.register_blueprint(webformlib, url_prefix='/api/webformlib')
        except disable_exception as e:
            logger.error('{0}启动【webformlib】模块失败，跳过！{0}'.format('×' * 15))
            logger.exception(e)
        else:
            logger.info('{0}【webformlib】模块启动成功{0}'.format('√' * 15))

    return app


# env 从环境变量中取到，TVTEST_ENV，线上为production，默认为default
app = create_app(env=env)


# CORS(app)
# 加载顶层视图函数，缺少下面的语句会导致views中的视图函数注册失败
# from .views import *


@app.before_request
def env_switch():
    """请求预处理，可以获取登录信息g"""
    current_endpoint = request.endpoint
    # logger.debug('current_endpoint={}'.format(current_endpoint))
    endpoint_head = None
    flask.g.customer_cookie = {
        'userid': request.cookies.get('userid'),
        'token': request.cookies.get('token')
    }
    flask.g.customer_header = {'User-Agent': request.headers.get('User-Agent')}
    # logger.info(flask.g.customer_cookie)

    if current_endpoint:
        endpoint_head = current_endpoint.split('.')[0]
    # 忽略列表
    ignore_endpoint_list = ['auth', 'favicon']
    if endpoint_head in ignore_endpoint_list or current_endpoint in ignore_endpoint_list:
        return


@app.after_request
def format_response(response):
    """格式化，规范服务响应格式"""
    if request.endpoint == 'favicon':
        return response
    if request.endpoint == 'tools.getMock':
        return current_app.response_class(response.json, mimetype='application/json; charset=UTF-8',
                                          headers=response.headers)

    logger.debug('格式化response')
    if not response.is_json:
        return response
    data_new = dict()
    # func = app.view_functions.get(request.endpoint)
    # # desc = extract_func_desc(func.__doc__)
    data = response.json
    if isinstance(data, dict):
        # 状态位
        if 'status' in data.keys():
            data_new['status'] = data['status']
            del data['status']
        else:
            if ('success' in data.keys() and not data['success']) or \
                    ('message' in data.keys() and '失败' in data['message']) or \
                    ('status' in data.keys() and data['status'] == -1):
                data_new['status'] = False
            else:
                data_new['status'] = True
        # 提示文字
        if 'message' in data.keys():
            data_new['message'] = data['message']
            del data['message']
        else:
            if 'message' in data.keys():
                data_new['message'] = data['message']
            else:
                data_new['message'] = ''
        # 节点信息
        if 'node' in data.keys():
            data_new['node'] = data['node']
            del data['node']
        else:
            data_new['node'] = request.path
        # 数据节点
        if len(data) == 0:
            data_new['data'] = None
        elif 'data' in data.keys():
            data_new['data'] = data['data']
            del data['data']
        else:
            data_new['data'] = data
    else:
        data_new['status'] = True
        data_new['message'] = ''
        data_new['node'] = request.path
        data_new['data'] = data
    logger.info(data_new)
    return current_app.response_class(json.dumps(data_new), mimetype='application/json; charset=UTF-8',
                                      status=response.status_code)


@app.errorhandler(Exception)
def error_handler_custom(myexception):
    """错误统一处理函数"""
    logger.debug('统一异常处理')
    logger.exception(myexception)
    if isinstance(myexception, TVException):
        return flask.jsonify(myexception.to_dict()), 400
    elif isinstance(myexception, NotFound):
        return flask.jsonify({'status': False,
                              'node': 'notfound',
                              'message': str(myexception)}), 404
    else:
        return flask.jsonify({'status': False,
                              'node': request.path,
                              'message': str(myexception)}), 500
