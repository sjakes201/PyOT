class Publisher:
    def __init__(self):
        self.subscribers = dict()
    def subscribe(self, sub, func):
        self.subscribers[sub] = func
    def unregister(self, sub):
        del self.subscribers[sub]
    def publish(self, option, data):
        for sub in self.subscribers:
            self.subscribers[sub](option, data)