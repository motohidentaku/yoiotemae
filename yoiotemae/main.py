#!/usr/bin/env python3
# coding:UTF-8

from argparse import ArgumentParser
import os
from importlib import import_module
import configparser
import re

def make_json(measurment, tags, data):
    """
    make json

    Parameters
    ----------
    measurmant : string
        influx measurment
    tasg : string
        influx tags
    data : array
        influx : fields

    Returns
    -------
    json_body : string
        json string

    """
    json_body = [
            {
                "measurement": measurment,
                "tags": tags,
                "fields": data
                }
            ]

    return json_body


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--config',
        help='APIトークンを指定します。省略した場合はTOKEN環境変数の値が利用されます。',
        default='./yoiotemae/config/para.config')
    excludes = set(['common.py'])
    topdir = os.path.dirname(__file__)
    ns_root = os.path.dirname(topdir)

    args = parser.parse_args()

    cfg = configparser.ConfigParser()
    #cfg.read("./yoiotemae/config/para.config")
    cfg.read(args.config)

    
    data = dict()
    for dirpath, _, filenames in os.walk(topdir):
        ns = os.path.relpath(
            dirpath, start=ns_root).replace('/', '.').replace('\\', '.') + '.'
        for fn in filenames:
            if not fn.endswith('.py') or fn.startswith('_') or fn in excludes:
                continue
            n, _ = os.path.splitext(fn)
            if cfg.has_section(n):
                in_para = [cfg[n][x] for x in cfg[n] if re.match(r'in_', x)]

                m = import_module(ns + n)
                instance  = getattr(import_module(ns + n), n.capitalize())(in_para)

                if hasattr(instance, 'get'):
                    for name, v in zip([x for x in cfg[n] if re.match(r'name', x)] ,instance.get()):
                        data[cfg[n][name]] = v

    print(make_json(cfg["server"]["measurement"], {"node": cfg["edge"]["nodename"], "location": cfg["edge"]["location"]}, data))

