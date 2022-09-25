# Functional programming

In object oriented programming, objects are treated as first class citizens
and functions and methods belong mostly to different objects and
mutate their state. In contrast, functions are considered the first
class objects in functional programming. Functions can even be
returned by other functions and should be composed. One of the key
ideas is that functions should (typically) be determinstic and not
dependent on local state and that data should be immutable. The idea
being that with immutable data, it is easier to track state over time
as different states of data have to live in different objects, making
the appearance of bugs easier to track. From experience, the simple
act of trying to not change the state of objects requires one to
be more explicit with data transformations and helps create
simpler, unit-testable functions.

## Pass by value

Pass by value means that when calling a function with parameter `x` a
new object `x` is created from the input and the input will not be
changed. In python, simple types can be thought of as pass by reference
as in the following example:

```python
def foo(x: int):
  x = 2

y = 1
foo(y)
print(y)
```

The final line will print out `1`.

## Pass by reference

However, except in simple cases as above, python is actuall passing by
reference, where new data is not created when invoking a function.

```python
class Entity:
  def __init__(self, name: str):
    self.name = name


def foo(e: Entity):
  e.name = "steve"


e = Entity("bob")
foo(e)
print(e.name)
```

This program will print `steve` not because the object pass into `foo`
was passed by a reference to the original object. In the previous example,
we got around the fact that python passes by reference by actually
creating a new object called `2` that we then assigned to the variable
that happened to have the same name as the input parameter.

For example, the following program will output `bob`:

```python
class Entity:
  def __init__(self, name: str):
    self.name = name


def foo(e: Entity):
  e = Entity("steve")


e = Entity("bob")
foo(e)
print(e.name)
```

## Drawbacks


Some operations are sort of inherently stateful. Imagine training
a very large (billions of parameters) neural net. The neural net might
only just fit into memory, so creating a new version of the neural net
for every run of backpropagation might not be feasible and updating
th neural net in place might be required.
