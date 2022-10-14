import numbers
import os
import sys
from typing import Dict, Any


class DataType:
    QUERY = "query"
    INSERT = "insert"


def main_process(pipe_send, pipe_receive):
    try:
        while True:
            item = pipe_receive.recv()
            if item == DataType.INSERT:
                print(f"insert with no return data.")
            if item == DataType.QUERY:
                print(f"query with return data.")
                pipe_receive.send(f"{item}'s result")
                # pipe_send.send(f"{item}'s result")
    except EOFError:
        pipe_receive.close()


def sub_process(pipe_send, pipe_receive):
    for item in range(10):
        if item % 2 == 0:
            pipe_send.send(DataType.INSERT)
        else:
            pipe_send.send(DataType.QUERY)
            res = pipe_send.recv()
            print(f"sub process receive res:{res}")
    # _i = pipe_out.recv()
    # print(_i)


def func(*f):
    print(f)


def raise_exception(is_raise: bool) -> bool:
    if is_raise:
        raise RuntimeError()
    return False


resource_names = {"cpu": numbers.Number, "gpu": int, "memory": numbers.Number}
attribute_names = ["request", "limit"]


def valid_resource(resources: Dict[str, Any]) -> None:
    for _name, _resource in resources.items():
        if _name not in resource_names:
            raise RuntimeError(f"resources name is illegal, name must in {resource_names.keys()}")

        if isinstance(_resource, numbers.Number):
            resources[_name] = {"request": _resource, "limit": _resource}
        elif isinstance(_resource, dict):
            if not all(n in attribute_names for n in _resource):
                raise RuntimeError(
                    f"resources value is illegal, attribute's name must in {attribute_names}"
                )
        print(f"origin:{_resource}, new:{resources[_name]}")

        for _k, _v in resources[_name].items():
            if not isinstance(_v, resource_names[_name]):
                raise RuntimeError(f"resource:{_name} only support type:{resource_names[_name]}, but now is {type(_v)}")

if __name__ == '__main__':
    # # 第一个进程管道发出数字
    # pipe_in, pipe_out = multiprocessing.Pipe(True)
    # # process_pipe_1 = multiprocessing.Process(target=create_items, args=(pipe_1,))
    # process_pipe_1 = threading.Thread(target=main_process, args=(pipe_in, pipe_out))
    # process_pipe_1.start()
    # # 第二个进程管道接收数字并计算
    # process_pipe_2 = multiprocessing.Process(target=sub_process, args=(pipe_in, pipe_out,))
    # process_pipe_2.start()
    # process_pipe_1.join()
    # process_pipe_2.join()

    _s = "T.Y.Z.Cls"
    prefix, delim, last = _s.rpartition(".")
    print(f"1.pre:{prefix}, delim:{delim}, last:{last}")
    _s = "func"
    prefix, delim, last = _s.rpartition(".")
    print(f"2.pre:{prefix}, delim:{delim}, last:{last}")

    _l = ["1", "2"]
    func("3", "5", "6")
    print("===")
    func(*_l)

    print("------")
    _d = {"1": "2", "3": "4"}
    for k, v in _d.items():
        print(f"k:{k}, v:{v}")

    print("++++++")
    raw = "ins/pro/mnist/version/latest"
    # ['ins', 'pro/mnist/version/latest']
    _sp = raw.split("/", 1)
    print(_sp)
    raw2 = "ins"
    # ['ins', 'pro/mnist/version/latest']
    _sp2 = raw2.split("/", 1)
    print(_sp2)

    pro = "pro/mnist/ /version///fsdfsdf"
    pro = pro.strip().strip("/")
    print(f"pro:{pro}")

    _h = "mvswkodbgnrtsnrtmftdgyjznrxg65y"
    _version = _h if False else _h[:12]
    print(_version)
    # res = True
    # try:
    #     res = raise_exception(True)
    #     print(f"success:{res}")
    # except Exception as e:
    #     print(f"error:{e}")
    # finally:
    #     if res:
    #         print("finally 0")
    #     else:
    #         print("finally -1")
    #         sys.exit(-1)
    ROOT_DIR = os.path.dirname(__file__)
    _abs = os.path.abspath(ROOT_DIR)
    print(_abs)
    os.environ["SW_TEST"] = "my_env"
    _url = os.environ.get("SW_TEST") or "test_env"
    print(f"env is :{_url}")

    os.environ["URL"] = "http://127.0.0.1:8082"
    print(f"now url is:{os.environ.get('URL')}")

    _resources = {
        "cpu": 0.1,
        "memory": 2,
        "gpu": 2.1,
    }
    #valid_resource(_resources)
    print("===")
    _resources2 = {
        "cpu": {
            "request": 0.1,
            "limit": 0.2,
        },
        "memory": 2,
        "gpu": {
            "request": 0.1,
            "limit": 0.2,
        }
    }

    #valid_resource(_resources2)

    print(isinstance("0.1", numbers.Number))

    print(int("7"))
    print(numbers.Real("0.7r"))


