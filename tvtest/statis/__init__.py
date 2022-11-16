#!/usr/bin/env python
# coding:utf-8

from flask import Blueprint

statis = Blueprint('statis', __name__)

from . import views
