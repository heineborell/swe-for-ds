# Two Web Frameworks

For this tag we have added two scripts that can be used
to serve the iris predictor that we have previously trained.
These frameworks make it very simple to setup web applications
and are commonly used to serve machine learning predictions. We
will not be setting up a frontend webpage that is viewable, but will
focus on setting up `GET` and `POST` routes
which could be called by another application and responsd via JSON.

The two scripts are in the `serving` folder which has its own requirements,
which also assumes that `someproject` has been installed in order
to use the predictor. Ideally this would be in a separete repository with
its own structure. Note that the structure of this directory does not
use a `setup.py` file as we are not creating a package, but an application
that is using packages. As such, we use a `requirements.txt` to capture
dependencies.

## Flask

The first, and more traditional, web framework is called [flask](https://flask.palletsprojects.com/en/2.2.x/).
As seen in the `flask_server.py` module, one creates a `Flask` object
then adds routes to it.
These routes are added by taking normal functions and then
decorating them with `@app.get` or `@app.post` and making sure that they
return an appropriate `Response` object. Functions which provide the logic
for routes are often called _handlers_.

Assuming that a `clf.pickle` file is present in `serving/artifact`,
the flask server can be run from within the `serving/` directory with
the command

```bash
flask --app src.flask_server:app --debug run --host 0.0.0.0 --port 8000
```

The `--debug` flag will allow the server to reload if it detects changes
in the source code, which is useful for both development and debugging.

To get a prediction from the `GET` route:

```bash
curl "localhost:8000/predictions?sepal_length=1.2&sepal_width=1.2&petal_length=1.2&petal_width=1.2"
```

To get a prediction from the `POST` route:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 1.2, "sepal_width": 1.2, "petal_length": 1.2, "petal_width": 1.2}" \
  localhost:8000/predictions
```

While the `GET` route might be good for single predictions with simple data types,
the `POST` route is more appropriate for getting batches of predictions and when you
have more complex data types.

Note that we have added helper functions in the flask serving script
to help us validate the data that we are receiving. This has been made
easier by the fact that we are using pydantic the `BaseModel` to define our
input and output data typees, but we have still written our own responses
based on the built in validation they provide.

## FastAPI

A more modern alternative to flask is [FastAPI](https://fastapi.tiangolo.com/), which
offers two imporvements over flask. The first, which we will take advantage of, is
that data validation using pydantic is built in. Comparing the FastAPI implementation
to the flask implementation, it is clear how much boilerplate we were able to remove.

Secondly, FastAPI allows for the routes to run concurrently. This is not so important
when serving compute intensive machine learning models, but if the application needs
to call other applications, this creates opportunities for massive speedups. This involves
using [asyncio](https://docs.python.org/3.10/library/asyncio.html) which is part of the
standard library and differs somewhat from the `concurrent.futures` library we
discussed previously. Since this is not as relevant to our use case, we will limit
ourselves to the mention in this paragraph.

To run the FastAPI application, we will use `uvicorn`, which is an ASGI server which
is appropriate for the asynchronous ready FastAPI application, even if we aren't using
these capabilities. The server can be started with

```bash
uvicorn src.fastapi_server:app --reload --port 8000
```

and predictions can be obtained using the same commands as above.

## Gunicorn

Flask warns the user not to use its development server in production,
and the standard server to use is [gunicorn](https://gunicorn.org/). In contrast
to the async compatible ASGI server we used with FastAPI, this is a synchronous
WSGI server. Using gunicorn allows us to control many things such as logging
styles, but most importantly gives us control over how many workers, i.e., processes,
we which to run at the same time, which gives us access to parallelism as we
serve the application. Gunicorn handles sending requests to the different workers
it controls. [Gunicorn configuration docs](https://docs.gunicorn.org/en/stable/configure.html)

To run the flask application using gunicorn from within the `serving/` directory with two workers:

```bash
gunicorn src.flask_server:app --bind 0.0.0.0:8000 --workers 2 --worker-class gevent
```

Since machine learning applications are synchronous, it still makes sense to use
multiple processes to serve the FastAPI application, and one can also use gunicorn
for this use case, as long as the worker class is compatible with asynchronous code
that FastAPI is using under the hood. To run the FastAPI server from within the
`serving/` directory:

```bash
gunicorn src.fastapi_server:app --bind 0.0.0.0:8000 --workers 2 --worker-class uvicorn.workers.UvicornWorker
```
