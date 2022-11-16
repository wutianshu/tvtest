#!/usr/bin/env python
# coding:utf-8

from flask import Blueprint

import os,logging

logger = logging.getLogger(__name__)


tools = Blueprint('tools', __name__)


# 必须在当前包的__init__文件中导入，否则引用
from .views import *
