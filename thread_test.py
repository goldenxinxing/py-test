import random
import threading
import time


class t(threading.Thread):
    def __init__(self):
        super().__init__()
        self._records = []
        self._cond = threading.Condition()
        self._cond2 = threading.Condition()
        self.setDaemon(True)
        self.start()

    def put(self, record: str):
        with self._cond:
            print(f"{threading.currentThread()} put record:{record}.")
            time.sleep(0.01*random.randint(1, 10))
            self._records.append(record)
            self._cond.notify()

    def flush(self):
        while True:
            with self._cond:
                if len(self._records) != 0:
                    print(f"{threading.currentThread()} flush waiting...")

                else:
                    with self._cond2:
                        print(f"{threading.currentThread()} flushing")
                        break
                self._cond.notify()
        print(f"{threading.currentThread()} flushed")

    def run(self) -> None:
        while True:
            with self._cond:
                while len(self._records) == 0:
                    print(f"{threading.currentThread()} writer waiting...")
                    self._cond.wait()
                if len(self._records) == 0:
                    print(f"{threading.currentThread()} have not records, break")
                    break
                records = self._records
                self._records = []
                print(f"{threading.currentThread()} writer release lock")

            with self._cond2:
                # release!!!!!!
                for r in records:
                    print(f"{threading.currentThread()} writer use record:{r}")


if __name__ == '__main__':
    _t = t()
    for i in range(10):
        _t.put(f"data-{i}")
    _t.flush()

    for i in range(10, 20):
        _t.put(f"data-{i}")

    _t.flush()

