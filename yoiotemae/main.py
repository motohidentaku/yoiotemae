#!/usr/bin/env python3
# coding:UTF-8

from argparse import ArgumentParser
import os
import errno
from importlib import import_module
from configparser import ConfigParser
import re
from influxdb import InfluxDBClient
from .common import (
    make_json)

def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--config',
        help='config filepath. default is ./yoiotemae/config/para.config',
        default='./yoiotemae/config/para.config')
    parser.add_argument(
        '--influx',
        help='influx url.指定しない場合はinfluxに送信しない')
    parser.add_argument(
       '--port',
        help='influx port. default is 8086',
        default=8086)
    parser.add_argument(
       '--dbmeasur',
        help='influx database:measurement default is sensor:Environment',
        default='sensor:Environment')
    excludes = set(['common.py'])
    topdir = os.path.dirname(__file__)
    ns_root = os.path.dirname(topdir)

    args = parser.parse_args()

    #read config file
    if not os.path.exists(args.config):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.config)
    cfg = ConfigParser()
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
    if args.influx:
        client = InfluxDBClient(host=args.influx, port=args.port, database=args.dbmeasur.split(':')[0])
        print(client.write_points(make_json(args.dbmeasur.split(':')[1],
            {"node": cfg["edge"]["nodename"], "location": cfg["edge"]["location"]}, data)))
    else:
        print(data)
