import multiprocessing
import threading


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


if __name__ == '__main__':
    # 第一个进程管道发出数字
    pipe_in, pipe_out = multiprocessing.Pipe(True)
    # process_pipe_1 = multiprocessing.Process(target=create_items, args=(pipe_1,))
    process_pipe_1 = threading.Thread(target=main_process, args=(pipe_in, pipe_out))
    process_pipe_1.start()
    # 第二个进程管道接收数字并计算
    process_pipe_2 = multiprocessing.Process(target=sub_process, args=(pipe_in, pipe_out,))
    process_pipe_2.start()
    process_pipe_1.join()
    process_pipe_2.join()
