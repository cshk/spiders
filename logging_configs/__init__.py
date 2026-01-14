#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------
# @Time     : 2025/6/20 11:23
# @Author   : zz
# @File     : log_config.py
# @Annotate :
# ----------------------------


import logging.config
import pathlib
import atexit
import json


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


def setup_logging():
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    with open(BASE_DIR / 'logging_configs/config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    # 替换占位符为实际路径
    config['handlers']['file']['filename'] = config['handlers']['file']['filename'].format(BASE_DIR=BASE_DIR)
    # 生成json格式日志
    config['handlers']['json']['filename'] = config['handlers']['json']['filename'].format(BASE_DIR=BASE_DIR)
    logging.config.dictConfig(config)
    # 日志队列
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


# 调用 setup_logging 初始化日志记录器
setup_logging()

# 提供一个全局的日志记录器对象供其他模块使用
logger = logging.getLogger("root")