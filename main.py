#!/usr/bin/env python3
# coding:UTF-8

import sys
import configparser
import importlib

def get(cfg):
    data = dict()
    if cfg.has_section('sensor1'):
        try:
            module = importlib.import_module('lib.sensor1')
            sensor1 = module.Sensor1(cfg.getint("sensor1", "bus_number"))
            ret = sensor1.get()

            data[cfg['sensor1']['name1']] = ret[0]
            data[cfg['sensor1']['name2']] = ret[1]
            data[cfg['sensor1']['name3']] = ret[2]
        except Exception as e:
            print(e)

    if cfg.has_section('sensor2'):
        try:
            module = importlib.import_module('lib.sensor2')
            sensor2 = module.Sensor2(cfg.getint("sensor2", "bus_number"), cfg.getint("sensor2", "ch"))
            ret = sensor2.get()

            data[cfg['sensor2']['name']] = ret
        except Exception as e:
            print(e)

    if cfg.has_section('sensor3'):
        try:
            module = importlib.import_module('lib.sensor3')
            sensor3 = module.Sensor3(cfg.getint("sensor3", "io"))
            ret = sensor3.get()

            data[cfg['sensor3']['name']] = ret
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
