from unittest import TestCase
from lib.sensor1 import Sensor1 

class TestSensor1(TestCase):
  def test_get_normal(self):
    sensor = Sensor1({1})
    self.assertEqual({1, 2, 3}, sensor.get())
  
  def test_input_fail(self):
    with self.assertRaises(Exception):
      sensor = Sensor1({1,2})
