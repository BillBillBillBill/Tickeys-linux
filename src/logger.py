#!/usr/bin/env python
#coding: utf-8
import logging
import sys

__author__ = 'Huang xiongbiao(billo@qq.com)'

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
fmt = logging.Formatter('[%(levelname)s] %(asctime)s %(filename)s[line:%(lineno)d] %(message)s')
sh.setFormatter(fmt)
logger.addHandler(sh)
