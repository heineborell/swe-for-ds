# REST and HTTP

In this tag we'll talk about some of the basic ideas
of sending information over the internet.

## REST endpoints

The most typical way to expose data, in our case a machine
learning model and its predictions, is via a REST endpoint.
We won't get into the full technical definition of REST
endpoints but but below are some core concepts.

### Client - server architecture

A core idea in a RESTful system is that there is a separation
between the client who is requesting something and the server
which receives requests, hosts and updates data, and and
responds to the requests.

### Statelessness

A REST endpoint should be stateless in the sense that one
client requests should be processed independently of one
other. This does not mean that requests and different times
always receive the same response, as underlying data can
change between requests. However, if request A does not change
any data, then whether request B is received and processed before
or after request A does not matter.

## HTTP

Most REST endpoints are exposed via HTTP, the Hypertext Transfer
Protocol. Just because a service is exposed via HTTP does not
imply that it is RESTful and vice versa, if a service is RESTful
it doesn't need to use HTTP. The two are very correlated though.

In the cases we are interested in, an HTTP request consists of the
following pieces
- An endpoint identified by a URL
- A method used to send the request
- A header of metadata about the request
- The body of the request which contains data from the sender

### Body

The body of the request contains the data we will be sending.
In machine learning applications, this is typically serialized as JSON.

### Header

There are several common metadata fields considered in the header, but
headers can contain arbitrary key-value string pairs.

- `Content-Type: <MIME-TYPE>`: The content type tells the server how to
interpret the data included in the body. The content type is typically
a [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types) and common values are `application/json` when sending json, `text/plain`
for text files, `text/csv` for CSVs, and `text/html` for webpages.
- `Accept: <MIME-TYPE>`: This tells the server what sort of response type the
server needs to receive.
- `Authorization: <some authorization>`: the value is a string that
indicates the requester should be given access to the data at the endpoint.
Common values are `Bearer <base64 encoded token>` and a base64 encoded
string of the form `username:password`.

### Methods

An HTTP request can be sent with one of several typical methods
each with a different purpose.

- A `GET` request is done to ask for data
- A `POST` request is done to ask that data be created
- A `PUT` request is done to create or update data
- A `DELETE` request is done to ask that some data be deleted


### URL

The general format of a URL is the following:

```
<SCHEME>://<USERNAME>@<HOST>:<PORT>/path/to/data?query=something
```

Under HTTP, the scheme will be `http`. Very similar to HTTP is
HTTPS with the scheme `https`. We will limit ourselves to saying that
the format is similar, but more secure due to encryption of data in
transit. Most data will travel, even between internal clients at a
company via HTTPS. We will mostly ignore the differences.

In most HTTP(S) requests, the username and `@` symbol are not needed
and the port is assumed to be 80 for HTTP and 443 for HTTPS. When
running services locally, often a different port such as 8080 is used
since 80 is already in use by the host system, in which case the
port must be included in the request.

Typically data is organized on the server in colletions. For example,
there will be a collection of models which can be said to each have
a collection of predictions (which are typically not stored on disk,
unlike traditional data). SO in order to get a prediction, one might
send a request to a URL of the form

```
https://some.company.com/models/modelname/predictions`
```

The order of the path being the collection, the id for the item within
the collection, and then the collection under that item.

The query section looks like a question mark followed by key-value
pairs of strings. Building on the previous example, we might
specify the data we want to go into the prediction as follows

```
https://some.company.com/models/modelname/predictions?x=1&y=1.2&foo=bar
```

#### `GET`

Typically, a `GET` request uses queries to pass parameters and
the body of the request is empty. Using `cURL`, a get request can
be sent as follows:

```bash
curl https://some.company.com/models/modelname/predictions?x=1.2&y=3.4
```

To specify that we expect to receive JSON back and not HTML, say, we
would send the request as

```bash
curl -H "Accept: application/json" <URL>
```

In this model one thinks about retrieving predictions which exist
under the form of the model (even if they are not saved to disk)
and the query parameters are used to locate the prediction.

#### `POST`

When sending more data, typically a `POST` request will be used
and query parameters are not used. An example of sending JSON
data via `POST` using `cURL`:

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Accept: application/json \
     -d '{"field1": 1.2, "field2": 3,4, "textField1": "hello world"}' \
     https://some.company.com/models/modelname/predictions
```

Both the `GET` and the `POST` requests are demonstrated in an
end to end test file under `tests/e2e/test_endpoint.py` for a
(for now) non-existent endpoint running on localhost, a/k/a the
machine running the test code.

### Status codes

A response will also look like a request with a body and
headers and will have a status code. These are between 100
and 599 with each group of 100 codes indicating a similar condition.

- 100s: not used often,but means the request sould continue
- 200s: success, usually `200` is the only code used
- 300s: redirection codes
- 400s: something is wrong with the request, i.e., client error
    - `400`: misc bad request
    - `401`: unauthorized (not sure who requester is)
    - `403`: forbidden (know the requester, but they can't do the action)
    - `404`: not found
    - `418`: I'm a teapot
    - `422`: unprocessable entity, can be used when the JSON in
in a request does not conform to the client's expections.
- 500s: something went wrong with on the server, not the client's fault.
Typically only `500` is used.

## Websockets

There are in reality multiple flavors of HTTP and we have been exclusively
talking about `HTTP/1` and `HTTP/1.1`. We have been sending a single request which
connects to the server which then gives a single response and closes
the connection. Under `HTTP/2`, connections can stay open and
multiple requests and responses can stream in and out before the connection
is closed. This is commonly referred to as using websockets. This is
technically possible under `HTTP/1.1`, but is not used often in practice.
The standard exposure of models is done under `HTTP/1.x`and websockets are
not used, but this is not a requirement.
