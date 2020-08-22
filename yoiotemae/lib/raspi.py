from .sensor import Sensor

import os
import subprocess
import re
import psutil

class Raspi(Sensor):

  def __init__(self, arg):
    self.argnum = 0

  def command_sh(self, command):
    proc = subprocess.check_output(command).decode('utf8').split('=')[1].rstrip('\n')
    return float(re.findall(r"[-+]?\d*\.\d+|\d+", proc)[0])

  def get(self):
    temp = self.command_sh(['vcgencmd', 'measure_temp'])
    clock = self.command_sh(['vcgencmd', 'measure_clock arm'])
    volt = self.command_sh(['vcgencmd', 'measure_volts'])
    arm = self.command_sh(['vcgencmd', 'get_mem arm'])
    gpu = self.command_sh(['vcgencmd', 'get_mem gpu'])
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=1)

    return [temp, clock, volt, arm, gpu, ram, cpu]

