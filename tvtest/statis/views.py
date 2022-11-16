#!/usr/bin/env python
# coding:utf-8

import logging
from flask import request, jsonify, render_template

from .models import APICallStatis, APICallItems
from . import statis
from tvtest import db
import pyecharts.options as opts
from pyecharts.charts import WordCloud

# 定义日志hander
logger = logging.getLogger(__name__)


@statis.before_app_request
def api_call_count():
    # 忽略列表
    ignore_endpoint_list = ['favicon', None]
    current_endpoint = request.endpoint
    current_path = request.path
    current_module = None
    current_method = None
    if current_endpoint:
        current_module = current_endpoint.strip().split('.')[0]
        current_method = current_endpoint.strip().split('.')[-1]
    if request.endpoint in ignore_endpoint_list or \
            current_module in ignore_endpoint_list or \
            current_path in ignore_endpoint_list:
        return
    try:
        items = APICallItems(endpoint=current_endpoint,
                             module=current_module,
                             method=current_method,
                             path=current_path)
        items.save()

        api = APICallStatis.query.filter_by(endpoint=current_endpoint).first()
        if api is None:
            api = APICallStatis(endpoint=current_endpoint,
                                module=current_module,
                                method=current_method,
                                path=current_path)
            api.save()
        api.call_count()
    except Exception as e:
        logger.exception(e)
        logger.error('接口访问统计模块【statis】在记录接口访问次数时报错，跳过……')


@statis.route('/info')
def api_call_info():
    api_name = request.values.get('api')
    if api_name:
        api_name = api_name.strip()
    else:
        return jsonify({'status': False,
                        'message': '必须携带api参数',
                        'node': 'statis'})

    api = APICallStatis.query.filter_by(endpoint=api_name).first() or \
          APICallStatis.query.filter_by(path=api_name).first() or \
          APICallStatis.query.filter_by(method=api_name).first()
    if api:
        return jsonify(api.to_json())
    else:
        return jsonify({'status': False,
                        'message': '没有找到你请求的接口【{}】统计信息'.format(api_name),
                        'node': 'statis'})


def data_show():
    data = db.session.query(APICallStatis.path, APICallStatis.count).filter(
        APICallStatis.last_access_time > '2021-01-01').all()
    (
        WordCloud()
            .add(series_name="数据工厂", data_pair=data, word_size_range=[15, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="数据工厂", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    ).render("/opt/soft/apache-jmeter-5.1.1/bin/projects/cstest_wordcloud.html")
    logger.info('任务执行成功，路径为：/opt/soft/apache-jmeter-5.1.1/bin/projects/cstest_wordcloud.html')


