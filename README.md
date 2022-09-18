# Type hints

Python is a __dynamically typed__ language, i.e., variables
can change types. On one line you can write `x=47` and have
`x` be an integer and three lines later within the same
code you can write `x="forty-seven"` and have `x` be a
string and python interpreter is perfectly happy. This is
particularly useful in interactive sessions where you might
be playing around with functionality and using `x` as a generic
variable name and not worrying about its value.

In contrast, there are programming languages, such as golang,
which are __statically typed__. If you initialize `x` as
an integer, you can't then say that `x` is going to be a
string later one. Since in most cases you don't want to re-use
variable names in the same context with different types,
this makes sense, even though python's choice is very convenient.

In addition, python doesn't have an inherent mechanism to check
that functions are being called with the correct type of object
and returning the correct type of object. Python is interpreted
not compiled, and most compiled languages can check during
build time of an application that functions are at minimum called
with the correct types of objects. While this might or might not
be possible for interpreted languages like python, it is not
implemented in python.

However, there is a
new-ish mechanism (python 3.5+) called __type hints__ which allow
us to mimic some of these behaviors and a tool called `mypy` that
allows us to check types as if the language were compiled and
statically typed.

Example:

```python
def foo(a: int, b list[int]) -> pd.Dataframe:
```

```python
from typing import Union


def foo(a: Union[int, float]):
```


Unfortunately, since type hints are not required by python, not
every package has type hints available. And often you have to
install a completely separte package of __stubs__ to get the
type hints for a package. This is also something you probably
only want to do in your development environment not in an
environment using the code, which leads to the awkwardconstruction

```python
from typing import TYPE_CHECKING


if TYPE_CHECKING:
  from type_hint_package import FooType


def foo() -> "Foo":
  pass
```
