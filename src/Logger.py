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
                stream[1].write(msg + '\n')

    def addTarget(self, path, logLevel=0):
        self.streams.append((logLevel, open(path, 'a')))
