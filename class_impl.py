class SuperClass:
    def __init__(self, i: int):
        self.index = i


class SubClass(SuperClass):
    def test(self):
        print(self.index)


if __name__ == '__main__':
    sub = SubClass(2)
    sub.test()
