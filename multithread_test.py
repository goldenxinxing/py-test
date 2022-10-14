import concurrent.futures
import random
import time

from thraedlocal_test import _at, lo


def execute(index: int) -> int:
    lo.index = index
    # time.sleep(random.randint(0, 3))
    _at()
    return lo.index


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(execute, index=i) for i in range(10)]
        res = [f.result() for f in concurrent.futures.as_completed(futures)]
        print(res)
