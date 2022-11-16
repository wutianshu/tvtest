# -*- coding:utf-8 -*-
from flask import Blueprint

# 新建蓝图
webformlib = Blueprint('webformlib', __name__)

from .views import *
