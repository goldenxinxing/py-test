import concurrent.futures
import multiprocessing
import atexit
import threading
from queue import Queue
from typing import List


class Final:
    def __init__(self, main: int, i: int):
        self.main = main
        self.i = i

    def final(self):
        with open("./test.txt", "a") as f:
            f.write(f'main:{self.main}-{self.i} final work \n')
        print(f'main:{self.main}-{self.i} final work')


def worker(main: int, i: int) -> bool:
    try:
        print(f'main:{main}-{i} Doing some work')
        f = Final(main, i)
        atexit.register(f.final)
        return True
    finally:
        # 必须得这么加，否则不行
        print("exit")
        # atexit._run_exitfuncs()


class Step:
    def __init__(self, index: int):
        self.status = "init"
        self.index = index


class Scheduler:
    def __init__(self, steps: List[Step]):
        self.steps = steps

    def schedule(self):
        queue = Queue()
        p = Producer(queue, self.steps)
        p.start()
        c = Consumer(queue)
        c.start()
        p.join()
        queue.join()


class Producer(threading.Thread):
    def __init__(self, queue: Queue, steps: List[Step]):
        super().__init__()
        self.steps = steps
        self.queue = queue
        self.current = 0

    def run(self) -> None:
        print('Producer starting')
        self.queue.put(self.steps[self.current])
        while True:
            if self.steps[self.current].status != "init":
                self.current += 1
                if self.current == len(self.steps):
                    print('Producer finished')
                    self.queue.put(None)
                    break
                else:
                    print('Producer one')
                    self.queue.put(self.steps[self.current])


class Consumer(threading.Thread):
    def __init__(self, queue: Queue):
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        print('Consumer starting')
        # process items from the queue
        while True:
            # get a task from the queue
            step = self.queue.get()
            # check for signal that we are done
            if step is None:
                break

            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=2
            ) as executor:
                futures = [executor.submit(worker, step.index, i) for i in range(3)]
                res = all(
                    future.result()
                    for future in concurrent.futures.as_completed(futures)
                )
            print(f"执行结果{res}")
            if res:
                print(f"执行完成")
                step.status = "success"
                print(f'.consumer got {step}')

                # mark the unit of work as processed
                self.queue.task_done()
        # mark the signal as processed
        self.queue.task_done()
        print('Consumer finished')


# 来源：https://superfastpython.com/thread-queue-task-done-join/
if __name__ == '__main__':
    # p = multiprocessing.Process(target=worker)
    # p.start()
    # p.join()
    _steps = [Step(0), Step(1), Step(2), Step(3)]
    s = Scheduler(_steps)
    s.schedule()
