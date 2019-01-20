from datetime import datetime

class Logger:
    def __init__(self):
        # List of tuples of write streams and log levels
        self.streams = []

    def __del__(self):
        for stream in self.streams:
            stream[1].close()

    def log(self, msg, logLevel=0):
        for stream in self.streams:
            if (stream[0] == logLevel):
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                stream[1].write(time + ' | ' + msg + '\n')

    def addTarget(self, path, logLevel=0):
        self.streams.append((logLevel, open(path, 'a')))
