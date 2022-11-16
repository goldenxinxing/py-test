import os
import subprocess
from typing import List, Tuple, Any

from loguru import logger


def invoke_with_react(args: List[str], input_content: str = "yes") -> Tuple[int, str]:
    return invoke(args, input_content=input_content)


def invoke(*args: List[str], input_content: str = None, raise_err: bool = False) -> Tuple[int, str]:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    p = subprocess.Popen(*args,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         env=env,
                         universal_newlines=True)
    if input_content:
        p.communicate(input=input_content)

    logger.debug(f"cmd: {p.args!r}")

    output = []
    while True:
        line = p.stdout.readline()  # type: ignore
        if line:
            logger.debug(line)
            output.append(line)

        if p.poll() is not None:
            break

    p.wait()
    for line in p.stdout.readlines():  # type: ignore
        if line:
            logger.debug(line)
            output.append(line)

    try:
        p.stdout.close()  # type: ignore
    except Exception as ex:
        logger.error(f"failed to close stdout:{ex}")

    if raise_err and p.returncode != 0:
        cmd = args[0]
        e = subprocess.CalledProcessError(p.returncode, cmd)
        e.output = "".join(output)
        raise e
    return p.returncode, "".join(output)


if __name__ == "__main__":
    code, res = invoke(["ls"])
    # logger.debug(f"code:{code}, res:{res}")
