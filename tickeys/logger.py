#!/usr/bin/env python
# coding: utf-8
import logging

# 创建一个logger
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于输出到控制台
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler("/tmp/tickeys.log")
fh.setLevel(logging.DEBUG)

# 定义handler的输出格式
# fhfmt = logging.Formatter(
#     '[%(levelname)s] %(asctime)s %(filename)s[line:%(lineno)d] %(message)s')
fhfmt = logging.Formatter(
    '%(message)s  -%(filename)s[line:%(lineno)d]')
shfmt = logging.Formatter(
    '%(message)s')
fh.setFormatter(fhfmt)
sh.setFormatter(shfmt)

logger.addHandler(sh)
logger.addHandler(fh)
logger.debug('test')
