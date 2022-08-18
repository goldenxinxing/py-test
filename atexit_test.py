import concurrent.futures
import multiprocessing
import atexit
import threading


def final(main: int, i: int):
    with open("./test.txt", "w") as f:
        f.write(f'main:{main}-{i} final work')
    print(f'main:{main}-{i} final work')


def worker(main: int, i: int):
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
            t = Executor(self.index, self)
            t.start()
            t.join()


class Executor(threading.Thread):
    def __init__(
        self,
        index: int,
        scheduler: Scheduler,
    ):
        super().__init__()
        self.scheduler = scheduler
        self.index =index

    def run(self) -> None:
        with concurrent.futures.ProcessPoolExecutor(
                max_workers=2
        ) as executor:
            futures = [executor.submit(worker, self.index, i) for i in range(3)]
            res = all(
                    future.result()
                    for future in concurrent.futures.as_completed(futures)
            )
        if res:
            self.scheduler.schedule()


if __name__ == '__main__':
    # p = multiprocessing.Process(target=worker)
    # p.start()
    # p.join()
    s = Scheduler(3)
    s.schedule()

