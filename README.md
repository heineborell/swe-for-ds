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

### Processes vs threads

To understand parallelism in general and in python in particular it
is necessary to talk about processes and threads. A process can
be thought of as a single running program. A process can be broken
up into threads encompassing units of work. Parallelism can be
achieved on architectures with multiple processors either by
running multiple processes at once or running a mutiple threads
under a single process.

The python interpreter acts on one process, and due to something
called the __global interpreter lock__ (GIL), also runs on only
one thread at a time eveni n multiple core architectures. This
makes parallelism in python difficult, hence the solution above
of calling into code written in C or Rust, languages that do
not have a GIL.

So, how do we get around the GIL?

### Multiprocessing

Multiprocess parallelism in python is achieved by spawning sub processes,
each of which has its own python interpreter and memory.
Of course the number of
processes that can run at the same time is limited by the number of
cores on the machine running the parent process. Parallelism properly
refers to this sort of approach in python. This can be done using
either of two packages built into the standard library:
[multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
or [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html).

Multiprocessing is most beneficial for operations which are __compute
bounded__, i.e., operations which require heavy computations on a single
machine. Vectorized operations fall into this category.

A simple example that might benefit from multiprocessing is an ensemble
model. Each model can be loaded into a separate process and compute its
estimate independently. The data is then shared with the parent process
which decides what the final estimate is. However, note that computers
also have limited memory, which can also limit the number of processes.

### Multithreading

In contrast to compute bounded programs, there are also situations that
are __I/O bounded__, i.e., input-output bounded. This occurs most commonly
when sending requests for data to another machine. In this case, one can
use multithreading within a single process. Even if the threads cannot
actually run at the same time due to the GIL, most of their time is
spent waiting for responses, not actually computing. This is an example
of __concurrency__, not parallelism. While python has a
[threading](https://docs.python.org/3.8/library/threading.html) library,
it is easier to use the thread pool executor from
[concurrent.futures](https://docs.python.org/3.8/library/threading.html)
which is also part of the standard library.

Note that even though in python only one thread can be computing at a time,
one can start as many threads as desired since the number of waiting threads
is not bounded.

### An example using both

It is somewhat common when processing data to split into multiple processes
each of which also uses multiple threads. The threads are used to retrieve
external data, each process then aggregates the thread results to compute
something, and returns the computed value to the main process which
aggregates from each of the sub processes. An example is included in
`scripts/preprocess_data.py`.

Unfortunately, there is no formula which decides how many processes
or threads to use for a given situation. While the number of cores provides
an upper bound on the number of processes, each process can have an unlimited
number of threads waiting at once. The most effective strategy will depend on
the exact balance of I/O bound waiting, compute time, and memory limits.
