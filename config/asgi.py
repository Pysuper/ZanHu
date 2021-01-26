#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：asgi.py
# Author   ：zheng xingtao
# Date     ：2021/1/26 15:34


import os
import sys

import django
from channels.routing import get_default_application

# TODO: 配置asgi的时候，需要结合当前文件的目录结构
# application加入查找路径中
app_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.append(os.path.join(app_path, 'zanhu'))  # ../zanhu/zanhu，应用的路径

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()
application = get_default_application()
