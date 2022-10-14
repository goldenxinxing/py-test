import random
import threading
import time
from queue import Queue


class t(threading.Thread):
    def __init__(self):
        super().__init__()
        self.batch = 10
        self.timeout = 30
        self.queue = Queue()
        self.setDaemon(True)
        self.start()

    def put(self, record: str):
        time.sleep(0.01*random.randint(1, 10))
        print(f"{threading.currentThread()} put record:{record}.")
        self.queue.put(record)

    def flush(self):
        while not self.queue.empty():
            print(f"{threading.currentThread()} wait flush...")
            time.sleep(0.1)
        print(f"{threading.currentThread()} flushing")
        print(f"{threading.currentThread()} flushed")

    def run(self) -> None:
        _times = 0
        while True:
            time.sleep(0.1)
            if self.queue.qsize() >= self.batch:
                _records = [self.queue.get(block=False) for i in range(self.batch)]
                for r in _records:
                    print(f"{threading.currentThread()} use record:{r}")
            elif self.queue.empty():
                continue
            else:
                if _times >= self.timeout:
                    print(f"{threading.currentThread()} not satisfy batch:{self.batch}, will use records:{self.queue.qsize()}")
                    _records = [self.queue.get(block=False) for i in range(self.queue.qsize())]
                    for r in _records:
                        print(f"{threading.currentThread()} use record:{r}")
                    _times = 0
                else:
                    _times += 1


if __name__ == '__main__':
    _t = t()
    for i in range(10):
        _t.put(f"data-{i}")
    _t.flush()

    for i in range(10, 20):
        _t.put(f"data-{i}")

    _t.flush()
