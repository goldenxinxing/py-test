import datetime
import random
import threading
import time


class t(threading.Thread):
    def __init__(self):
        super().__init__()
        self._records = []
        self._updating_records = []
        self._cond = threading.Condition()
        self.setDaemon(True)
        self.start()

    def put(self, record: str):
        with self._cond:
            print(f"{threading.currentThread()} put record:{record}.")
            time.sleep(0.01 * random.randint(1, 10))
            self._records.append(record)
            self._cond.notify()

    def flush(self):
        while True:
            with self._cond:
                if len(self._records) != 0 or len(self._updating_records) != 0:
                    # print(f"{threading.currentThread()} flush waiting...")
                    continue
                else:
                    print(f"{threading.currentThread()} flushing")
                    break
        print(f"{threading.currentThread()} flushed")

    def run(self) -> None:
        while True:
            print(f"writer loop again......")
            with self._cond:
                while len(self._records) == 0:
                    print(f"{threading.currentThread()} writer waiting...")
                    self._cond.wait()
                if len(self._records) == 0:
                    print(f"{threading.currentThread()} have not records, break")
                    break
                self._updating_records = self._records
                self._records = []
                print(f"{threading.currentThread()} writer release lock")

            # release!!!!!!
            try:
                for r in self._updating_records:
                    print(f"{threading.currentThread()} writer use record:{r}")
                    time.sleep(1)
                    if r == "data-19":
                        raise RuntimeError("error")
            except Exception:
                print(f"{threading.currentThread()} error")
                break
            finally:
                self._updating_records = []


if __name__ == '__main__':
    _t = t()
    start = datetime.datetime.now()
    _t.flush()
    print(f"1- flush cost:{datetime.datetime.now() - start}")
    for i in range(10):
        _t.put(f"data-{i}")
    start = datetime.datetime.now()
    _t.flush()
    print(f"2- flush cost:{datetime.datetime.now() - start}")

    for i in range(10, 20):
        _t.put(f"data-{i}")

    start = datetime.datetime.now()
    _t.flush()
    print(f"3- flush cost:{datetime.datetime.now() - start}")
