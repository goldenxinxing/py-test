import concurrent.futures
import multiprocessing
import atexit
import threading


class Final:
    def final(self, main: int, i: int):
        with open("./test.txt", "a") as f:
            f.write(f'main:{main}-{i} final work \n')
        print(f'main:{main}-{i} final work')


def worker(main: int, i: int) -> bool:
    try:
        print(f'main:{main}-{i} Doing some work')
        f = Final()
        atexit.register(f.final, main, i)
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
    for _i in range(3):
        with concurrent.futures.ProcessPoolExecutor(
                max_workers=2
        ) as executor:
            futures = [executor.submit(worker, _i, i) for i in range(3)]
            res = all(
                future.result()
                for future in concurrent.futures.as_completed(futures)
            )



