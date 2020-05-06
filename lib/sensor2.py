from lib.sensor import Sensor

class Sensor2(Sensor):
  def __init__(self, bus_number):
    self.argnum = 2
    self.ch = bus_number[1]


  def get(self):
    return {1}
