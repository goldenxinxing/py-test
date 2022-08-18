import concurrent.futures
import multiprocessing
import atexit
import threading
from time import sleep


def final(main: int, i: int):
    print(f'main:{main}-{i} final work')


def worker(main: int, i: int) -> bool:
    try:
        print(f'main:{main}-{i} Doing some work')
        atexit.register(final, main, i)
        return True
    finally:
        # 必须得这么加，否则不行
        print()
        #atexit._run_exitfuncs()


class Scheduler:
    def __init__(self, index: int):
        self.index = index

    def schedule(self):
        self.index -= 1
        if self.index >= 0:
            with concurrent.futures.ProcessPoolExecutor(
                    max_workers=2
            ) as executor:
                futures = [executor.submit(worker, self.index, i) for i in range(3)]
                res = all(
                    future.result()
                    for future in concurrent.futures.as_completed(futures)
                )
            print(f"执行结果{res}")
            if res:
                print(f"执行完成")
                self.schedule()
            # e = Executor(self.index, self)
            # e.start()
            # e.join()


class Executor(threading.Thread):
    def __init__(
        self,
        index: int,
        scheduler: Scheduler,
    ):
        super().__init__()
        self.scheduler = scheduler
        self.index = index
        self.setDaemon(True)

    def run(self) -> None:
        with concurrent.futures.ProcessPoolExecutor(
                max_workers=2
        ) as executor:
            futures = [executor.submit(worker, self.index, i) for i in range(3)]
            res = all(
                    future.result()
                    for future in concurrent.futures.as_completed(futures)
            )
        print(f"执行结果{res}")
        if res:
            print(f"执行完成")
            self.scheduler.schedule()


class Step:
    def __init__(self, index: int):
        self.status = "init"
        self.index = index

if __name__ == '__main__':
    # p = multiprocessing.Process(target=worker)
    # p.start()
    # p.join()
    steps = []
    steps.append(Step(1))
    steps.append(Step(2))
    steps.append(Step(3))
    s = Scheduler(3)
    s.schedule()
    sleep(10)

