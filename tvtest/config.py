#!/usr/bin/env python
# coding:utf-8

import os
import platform


class Config(object):
    # flask表单密钥
    SECRET_KEY = os.environ.get("SECRET_KEY") or "TVTEST_2022"
    # 防止返回的json中汉字被转码
    JSON_AS_ASCII = False

    # 模块化加载

    # 统计模块开关
    STATIS = True
    # 认证权限开关
    AUTH = True
    # 小工具模块开关
    TOOLS = True
    # 表单实验室
    WEBFORMLIB = True


    PYTHON_VERSION = platform.python_version()
    # 调试语句：需要忽略模块加载异常时赋值为Exception，需要查看模块加载详细异常信息时赋值为ZeroDivisionError
    EXCEPTION = Exception

    # DB地址
    DB_HOST = os.environ.get('TVTEST_HOST')
    # DB端口
    DB_PORT = os.environ.get('TVTEST_PORT', 3306)  # 给默认值，防止windows平台下报错
    # DB用户名
    DB_USER = os.environ.get('TVTEST_USER')
    # DB密码
    DB_PASS = os.environ.get('TVTEST_PASS')
    # DB数据库
    DB_NAME = os.environ.get('TVTEST_DB')

    # 数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if AUTH or STATIS:
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4'.format(DB_USER,
                                                                                               DB_PASS,
                                                                                               DB_HOST,
                                                                                               DB_PORT,
                                                                                               DB_NAME)

    # 定时任务
    JOBS = [
        # {
        #     'id': 'bugSyc',
        #     'func': 'cstest:tools.views.bugSyc',
        #     'trigger': 'interval',
        #     'seconds': 60 * 60 * 6
        # },
        # {
        #     'id': 'task_bug_list',
        #     'func': 'cstest:views._task_remind',
        #     'args': ['bug_list'],
        #     'trigger': 'cron',  # 指定任务触发器 cron
        #     'day_of_week': '0-4',  # 每周1至周5晚上6点执行
        #     'hour': 18,
        #     'minute': 00
        # },
        # {
        #     'id': 'task_todo_list',
        #     'func': 'cstest:views._task_remind',
        #     'args': ['todo_list'],
        #     'trigger': 'cron',  # 指定任务触发器 cron
        #     'day_of_week': '0-4',  # 每周1至周5早上9点执行
        #     'hour': 9,
        #     'minute': 00
        # },
        # {
        #     'id': 'task_analyses_list',
        #     'func': 'cstest:views._task_remind',
        #     'args': ['analyses_list'],
        #     'trigger': 'cron',  # 指定任务触发器 cron
        #     'day_of_week': '0',  # 每周一10点运行
        #     'hour': 10,
        #     'minute': 00
        # },
        # {
        #     'id': 'show',
        #     'func': 'cstest:statis.views.data_show',
        #     'trigger': 'interval',
        #     'seconds': 60 * 60 * 6
        # },
    ]
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    SCHEDULER_API_ENABLED = True
    SCHEDULER_API_PREFIX = '/scheduler'
    SCHEDULER_ALLOWED_HOSTS = ['*']

    # SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 10}}

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    """线上配置"""
    pass


# 测试环境配置，默认配置
class DevConfig(Config):
    STATIS = True
    AUTH = True
    TOOLS = True
    WEBFORMLIB = True


config = {
    "production": ProdConfig,
    "default": DevConfig,
}
