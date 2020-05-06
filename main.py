#!/usr/bin/env python3
# coding:UTF-8

import sys
import configparser
import importlib
import re

def get(cfg):
    data = dict()
    for sec in filter(lambda x: re.match(r'sensor', x), cfg):
        try:
            module = importlib.import_module(cfg[sec]['filepath'])
            in_para = [cfg[sec][x] for x in cfg[sec] if re.match(r'in_', x)]
            instance  = getattr(module, cfg[sec]['classname'])(in_para)
            for name, v in zip([x for x in cfg[sec] if re.match(r'name', x)] ,instance.get()):
                data[cfg[sec][name]] = v
        except Exception as e:
            print(e)

    return make_json(cfg["server"]["measurement"], {"node": cfg["edge"]["nodename"], "location": cfg["edge"]["location"]}, data)


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
    args = sys.argv

    cfg = configparser.ConfigParser()
    cfg.read("./config/para.config")
    print(get(cfg))


if __name__ == '__main__':
    main()
