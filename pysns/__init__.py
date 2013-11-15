# -*- coding: utf-8 -*-


import os
import sys


__version__ = '0.0.3'


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, ROOT_DIR)


def get_client(name, *args, **kwargs):
    '''
    获取认证客户端

    client = get_client('weibo', client_id, client_secret, redirect_uri)
    '''
    return get_client_class(name)(*args, **kwargs)


def get_client_class(name, **kwargs):
    '''
    获取认证客户端类

    cls = get_client_class('tencent_weibo')
    client = cls(client_id, client_secret, redirect_uri)
    '''
    cls_name = _get_cls_name(name)
    module = __import__('adapter.%s' % name, fromlist=[cls_name])
    return getattr(module, cls_name)


def _get_cls_name(name):
    items = []
    for item in name.split('_'):
        items.append(item[:1].upper() + item[1:])
    return ''.join(items)
