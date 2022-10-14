import threading

lo = threading.local()


def _at():
    print(lo.index)
