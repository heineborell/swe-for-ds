# Serialization

Generally when talking about objects in python,
everything from built in lists of integers to
dataframes to sci-kit learn or pytorch models,  we are
thinking of the versions of them which exist in memory.
However, moving data and models around requires either
saving the models or data to disk or perhaps sending and
receiving a request over the internet.

To do this, we talk about __serializing__ (some languages
use the term __marshalling__) objects.

## To disk

### Data

For this section, we will consider our in memory object to
be a pandas dataframe. The most basic way to save the
dataframe is to save it as a CSV -- comma seperated value
text value. Note that CSV is a generic term, and data can
be separated by spaces, tabes, colons, or whatever other
special character that is desired. When tabs are used, the
file format is often called a TSV. At the end of the day,
CSVs are simply text files which have a particular format
and are human readable.

Another way to save data is as a parquet file. These files
are column based storage that can partition data into chunks
based on column values. A parquet file is often a directory
of parquet files which are automatically created based on
the desired partitioning. The columnar format means it is
possible to load slices of the data based on column values.
Parquet files can also save the data in more compressed
manner than in the plain text file CSVs. Parquet files
are not meant to human readable, and have to be interfaced
with by libraries such as [fastparquet](https://fastparquet.readthedocs.io/en/latest/)
or [pyarrow](https://arrow.apache.org/docs/python/index.html).
Note that pandas is able to use these libraries to
read and write dataframes to parquet files.

### Models

To serialize generic objects, python has the [pickle](https://docs.python.org/3/library/pickle.html)
package in the standard library. This is a common way to
save models created in sci-kit learn so that they can then be retrieved
and used by other code after training time.
Pickled objects are often saved into files with the ending
`.pickle` or `.pkl`.

Typically functions an be pickled -- remember, everything in
python is an object -- but functions which are defined as closures
are not picklable. The below code, although contrived,
will produce an `AttributeError`

```python
import pickle

def get_closure(a):
    def closure(b):
        return a*b
    return closure

closure_func = get_closure(2)

with open("closure_func.pickle", "wb") as f:
    pickle.dump(closure_func, f)
```

Other downsides of pickling is that it is python specific and
pickled objects cannot be transferred to other languages. Pickling
large amounts of data such as numpy arrays can be very inefficient.
The external package [joblib](https://joblib.readthedocs.io/en/latest/persistence.html)
can be used in this case.

A notable model object which is typically not pickled is a neural
net. Typically neural nets are written in a framework such as
[pytorch](https://pytorch.org/tutorials/beginner/saving_loading_models.html#what-is-a-state-dict)
or [tensorflow](https://www.tensorflow.org/tutorials/keras/save_and_load),
each of which have their own formats to save models. These formats
often can be interpreted by other frameworks and languages. Note that
it is often of interest to save a model to another format, such as
[ONNX](https://pytorch.org/tutorials/advanced/super_resolution_with_onnxruntime.html)
in order to use it in a different, perhaps faster, runtime environment.

## Between languages

In a previous video we spoke about how python code often calls into
C or Rust to compute things more efficiently. When this is done, the python
objects must be serialized into a format that the called language understands
and the responses must be deserialized into a format that python can read.

## Over the wire

In addition to serializing data in order to save it to disk
and deserializing it later, data must also be serialized to a format
to be sent over the internet and deserialized upon receipt.

The most common way to send data (when there is not too much data to send)
is via JSON: javascript object notation. An example of json is
the following:

```json
{
  "someText": "a text string here",
  "someNumber": -0.47,
  "someOtherNumber": 2,
  "someBoolean": true,
  "someList": ["a", "b", "c"],
  "otherObject": {
    "subfield": "hellow world"
  }
}
```

Even though it has javascript in the name, JSON is a simple
text serialization of data using some rules. It has the basic
datatypes of strings, numbers, floats, and arrays in addition
to the objects in the name which resemble python dictionaries
with strings as the keys.

Not just used for sending data over the internet, JSON can
be used to serialize other objects and is a common format alongside
YAML to save configuration for programs and infrastructure.

Another example of serialization is using `base64` encoding to
encode binary data as a string which can then be sent over the
wire. An image can be base64 encoded for example on the command
line using `base64 image.jpeg > image_base64.txt` and then
decoded with `base64 -d image_base54.txt > image_2.jpeg`. Python
has a buit in base64 library. Note that this is an encoding but
NOT encryption -- anyone can decode a base64 encded string to
its original format.
