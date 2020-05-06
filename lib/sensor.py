class Sensor:
  def __init__(self, arg):
    self.argnum = 1
    self.argcheck(arg)
    self.arg = arg

  def argcheck(self, arg):
    if len(arg) != self.argnum:
      raise TypeError(self.__class__.__name__ + ' 設定ファイルのパラメータが不正です')

  def get(self):
    return {}
