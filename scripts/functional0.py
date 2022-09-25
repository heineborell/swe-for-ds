def foo(x: int):
    x = 2  # noqa


y = 1
foo(y)
print(y)
