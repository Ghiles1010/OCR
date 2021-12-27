class B:
    def __init__(self, i):
        print(i.x)

class A:

    def __init__(self, x):
        self.x = x
        B(self)

A(4)