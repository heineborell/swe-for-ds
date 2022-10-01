# Parallelism

We'll talk about some ways to speed code up by trying
to do multiple things at once.

## Vectorization

The first way to do multiple things at once is to vectorize
your code. Think of this as instead of using a for loop to
apply a function to each element of a list in series, but
running the same function over all the elements in parallel.

### Two examples

Using `numpy` directly and the ipython magic `%timeit`:

```python
In [1]: import numpy as np
In [2]: x = np.array([1=*100, dtype=np.int64)
In [3]: %timeit x*2
In [4]: def multiply(x):
   ...:     for i in range(len(x)):
   ...:         _ = x[i]*2
   ...:

In [5]: %timeit multiply(x)
```

You should see an order of magnitude difference between
the vectorized result curtesy of numpy and the non-vectorized
for loop.

Another example is to use pandas which typically relies on
numpy's vectorization. Again, using ipython we can do the
following:

```python
In [1]: import pandas as pd
In [2]: df = pd.DataFrame({"x": [2.0]*100, "y": [1.0]*100})
In [3]: %timeit df["pct"] = 100 * (df["x"] / df["y"])
In [4]: def calc_pct(row):
   ...:     return 100 * (row["x"] / row["y"])
   ...:

In [5]: %timeit df["pct_2"] = df.apply(calc_pct, axis=1)
```

Once again, you should see about an order of magnitude difference
between the first, vectorized example and the second, non-vectorized
example.

However, since we are relying on numpy, we will not see the same
speedup when using string operations.

```python
In [1]: import pandas as pd
In [2]: df = pd.DataFrame({"sentence": ["hello world"]*100})
In [3]: %timeit df["len"] = df["sentence"].str.split().apply(len)
In [4]: def get_len(s):
   ...:     return len(s.split())
   ...:

In [5]: %timeit df["len2"] = df["sentence"].apply(get_len)
```

You should actually see that the second example is faster when
pandas cannot rely on numpy to vectorize the calculation in C.

(These pandas examples adapted from [here](https://pythonspeed.com/articles/pandas-vectorization/#:~:text=Be%20aware%20of%20the%20multiple,t%20use%20native%20code%20loops.))

### How

In some sense, python cannot do things in parallel. Python
has something called the __Global interpreter lock__ which
means that the python interpreter which is running your
program can only be processing one thing at a time. So
how do we get around that? What numpy is actually doing
is calling into pure C code which does have true parallelism.

This is a common pattern you will see. The way to make your
python code faster, is to call into some other language, typically
C, C++, or rust. For example, the library [polars](https://www.pola.rs/)
implements dataframes with an API similar to pandas but which
is more aggressive about calling Rust under the hood, while pandas
typically relies on numpy as an intermediary to call into C.

## Native python "parallelism"

In addition to calling into another language, there are two
other ways to have some form of parallelism when writing python.

The reason to put parallelism in quotes is that we want to
distinguish between two concepts: __parallelism__ and __concurrency__.

### Multiprocessing

Parallelism occurs when your computer is actually processing two things
at the same time. Your computer will have multiple cores, and you can use
these cores somewhat independently.

### Multithreading

In contrast to the parallel processing of using multiprocessing, there is
multithreading, which splits a program into threads which shrae cores.
This is using __concurrency__: an individual thread does multiple things
but tries to alternate between the processes when possible. In particular,
this is useful for operations which are __I/O bound__. Think of calling to
an external database to get information or calling an endpoint and waiting
for a response. A thread can make one call and while waiting for a response,
make the second call since the thread does not have to do anything during
the waiting process. The parallelism is really happening elsewhere, and our
computer can wait while the work is done somewhere else and transmitted back
to us.

### An example using both
