@staticmethod
def foo(x):
    print("executing foo(%s)" % (x))

class A:
    foo = foo

a = A()
a.foo('hi')