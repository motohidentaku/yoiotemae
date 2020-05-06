class Sensor2:
  def __init__(self, bus_number):
    self.bus_number = bus_number[0]
    self.ch = bus_number[1]


  def get(self):
    return {1}
