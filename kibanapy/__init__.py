#!/usr/bin/env python
# encoding: utf-8

__version__ = '0.1.4'
__release_date__ = '2015-08-02'


try:
    from .dashboard import Dashboard
    from .visualization import Visualization
except Exception:
    # setup.py import module 来获取__version__时，
    # 如果是纯净的环境没有安装一些依赖库，导入就会报错。
    # 如：requests 包依赖。所以这里用异常包裹导入异常
    pass
