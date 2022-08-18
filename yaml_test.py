from collections import defaultdict

import yaml
import typing as t


class Step:
    def __init__(
            self,
            job_name: str,
            step_name: str,
            resources: t.List[str],
            needs: t.List[str],
            concurrency: int = 1,
            task_num: int = 1,
            status: str = "",
    ):
        self.job_name = job_name
        self.step_name = step_name
        self.resources = resources
        self.concurrency = concurrency
        self.task_num = task_num
        self.needs = needs
        self.status = status

    def __repr__(self) -> str:
        return (
                "%s(job_name=%r, step_name=%r, resources=%r, needs=%r, concurrency=%r, task_num=%r, status=%r)"
                % (
                    self.__class__.__name__,
                    self.job_name,
                    self.step_name,
                    self.resources,
                    self.needs,
                    self.concurrency,
                    self.task_num,
                    self.status,
                )
        )


if __name__ == '__main__':
    _y = """
        default:
                - concurrency: 3
                  job_name: default
                  needs: []
                  resources:
                  - cpu=1
                  step_name: ppl
                  task_num: 6
                - concurrency: 1
                  job_name: default
                  needs:
                  - ppl
                  resources:
                  - cpu=1
                  step_name: cmp
                  task_num: 1
        """
    # rt: t.Dict[str, t.List[Step]] = {}

    rt = defaultdict(list)
    _jobs = yaml.safe_load(_y)
    for k, v in _jobs.items():
        rt[k] = [Step(**_v) for _v in v]

    print(rt)
