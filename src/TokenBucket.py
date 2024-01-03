import time
from threading import Lock

class TokenBucket:
    def __init__(self, capacity, fill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.fill_rate = fill_rate
        self.timestamp = time.time()
        self.lock = Lock()

    def _refill(self):
        now = time.time()
        elapsed_time = now - self.timestamp
        self.tokens = min(self.capacity, self.tokens + elapsed_time * self.fill_rate)
        self.timestamp = now

    def consume(self, tokens):
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                return False
