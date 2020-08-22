from .sensor import Sensor

import requests
import json

class Natureremo(Sensor):

  def __init__(self, arg):
    self.argnum = 1

    self.token = arg[0]

  def get(self):

    url = 'https://api.nature.global/1/appliances'
    headers = {
      'Authorization': 'Bearer ' + self.token
    }

    res = requests.get(url, headers=headers)
    instant = 0
    cumulative = 0
    coefficient = 0
    digits = 0

    for v in json.loads(res.text):
        if 'smart_meter' in v:
            for w in v["smart_meter"]["echonetlite_properties"]:
                if 'measured_instantaneous' in w.values():
                    instant = int(w["val"])
                if 'normal_direction_cumulative_electric_energy' in w.values():
                    cumulative = float(w["val"])
                if 'coefficient' in w.values():
                    coefficient = float(w["val"])
                if 'cumulative_electric_energy_effective_digits' in w.values():
                    digits = float(w["val"])
    if cumulative != 0 and coefficient != 0 and digits != 0:
        return [instant, cumulative * coefficient / 10 / digits]
    else:
        return [0, 0]
