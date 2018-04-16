import threading


class ThreadManager(object):

    def __init__(self):

        self.threads = threading.enumerate()
        print(self.threads)
