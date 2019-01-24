from datetime import datetime

class Logger:
  def __init__(self):
    # List of tuples of write streams and log levels
    self.streams = []

  def __del__(self):
    for stream in self.streams:
      stream[1].close()

  def log(self, msg, log_level=0):
    for stream in self.streams:
      if (stream[0] == log_level):
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stream[1].write(time + ' | ' + msg + '\n')

  def addTarget(self, path, log_level=0):
    self.streams.append((log_level, open(path, 'a')))
