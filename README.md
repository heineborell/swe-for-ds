# (Docker) Containers

We have previously written two servers that can work locally,
but how do we package up our code and serve it somewhere else?
The modern answer to this question is to use __containers__,
usually __docker containers__ (one implementation of an
open standard) to
package up code and its dependencies for deployment
onto a server. We'll introduce the core concepts behind this,
but the quick way to think about containers is that they
are akin to very lightweight virtual machines that are
separated from whatever else is running on the machine that is
running the container. We will talk about how this is not quite
true and their limitations as well.

We will be using [docker](https://www.docker.com/) to build
and run our containers and should be avilable for most operating
systems and architectures. Docker desktop is free for individuals
as well as small companies.

## Building images

An __image__ is the packaged up environment and code along with
running instructions. Images are typically stored in image
__registries__ with different images belonging to __repositories__
within the registry and organized by __tags__. As an example,
we can run `docker images` to see the images that we have on our
machine to see the image names (which correspond to repositories)
and tags. Image registries can be public or privately administered
by the companies using the images. We will only work with public
images.

An image is built from a base image and is built up in layers. This
can be seen by looking at the `Dockerfile` which defines the image
we want to build. We see that we are starting with the `python:3.10`
image, i.e., a publicly available image which comes with
python 3.10 already installed inside of it. In the course of
building the image, we see that we are copying our dependencies inside
of the image and installing them, as well as copying in our code
and the model artifact. We also specify what command should run upon
starting the image and which port should be exposed.

To build the image, run

```bash
docker build --tag iris-server:v0.1.0 .
```

to build an image with name `iris-server` and tag `v0.1.0`. If no
tag is specificed, the default is `latest`. When building, docker
will automatically pull the base image, but it can also be pulled
manually with `docker pull python:3.10`.

To remove an image, run `docker rmi <IMAGE_NAME>:<TAG>` or
`docker rmi <SHA>`.

Note that we have added a `.dockerignore` file to prevent
extraneous files from being added into the build context of
our dockerfile.

## Running containers

A __container__ is a running image. The philosophy of containers
is that a container should run one process. If a website has a frontend
and a backend and a database, these processes will all be running in
separate containers. We will briefly see later how to combine different
containers into a single service.

To run our container with the default command, we can simply run

```bash
docker run --name iris_1 -p 8080:8080 iris-server:v0.1.0
```

We have named the container `iris_1` and said that we want port 8080 on our
machine to correspond to port 8000 on the container. (Note: we could have
just as well mapped port 8000 on our local machine to port 8000 of the container.)
We can then curl to the container to get a prediction exactly as before:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 1.2, "sepal_width": 1.2, "petal_length": 1.2, "petal_width": 1.2}' \
  http://localhost:8000/predictions
```

To see the running containers, use `docker ps` and to see running and stopped
containers, use the command `docker ps -a`. Containers can be stopped with the
`docker stop` command and removed with the `docker rm` command.

Containers can also be started with alternate commands. For example, to open a
bash prompt within the container, one can run

```bash
docker run --rm -i -t iris-server:v0.1.0 bash
```

We added the flags `-i` and `-t` to make the container interactive and attach
our prompt to it, respectively. The `--rm` flag tells docker to remove
the container automatically when stopped. Running bash inside the container
allows us to inspect the image.

## Further topics

### Platforms

The big difference between containers and virtual machines is that containers
are dependent on the underlying operating system. This allows them to be
much lighter weight than virtual machines which must include everything
related to the operating system as well. The downside is that it might be
impossible to run a container built for a windows machine on a machine running
linux. Similarly, the architecture of the machine where the container was built
plays an important role.

To specify the family of operating systems and architecture, one can use the
`--platform` option when building. For example, I have an `x86` architecture
running linux, so building without the `--platform` tag is equivalent to running

```bash
docker build --platform linux/amd64 .
```

If I want to run the container on a Mac OS with an M1 chip, for example, I would
have to build the container as follows:

```bash
docker build --platform linux/arm64 .
```

(The `linux` part is correct, as Mac OS is unix-like.) An image name and tag can
exist for multiple architectures, and docker will pull the correct one for your
machine if possible. Some images built for different architectures might run
on your machine regardless, but will usually be slower and might have bugs.

### Secrets

It is common to need secrets (passwords, SSH keys, etc) when building images.
An example is that the image build process requires downloading a file from
a company database or installing a proprietary python package. In order to
avoid the secret being extractable from the built image, there is a `--secret`
option that can be used at build time. For example suppose there is a file
locally called `password.txt`, to make it available to during the build
process, one can build with the command

```bash
docker build --secret id=password,src=password.txt .
```

while simultaneously having in the dockerfile the line

```
RUN --mount=type=secret,id=password,dst=/some/path/password.txt COMMAND
```

and `password.txt` will be available inside the image at `/some/path/password.txt`
during the running of `COMMAND`.
Note that using this might require the docker buildkit, which can be enabled by
setting the environment variable `DOCKER_BUILDKIT=1`.

This is not the only way to handle secrets, but is a common way to use them.

### Volumes

Running containers have a filesystem that is separate from the machine it is
running on, but you can mount a volume from your filesystem to the container. This
allows a container to write to a file that then persists on the host machine
after the container is removed and allows one to load files from the local machine
to a running container, for example code changes can be loaded into the container
for testing or development purposes. Using the full path on both the host machine
and the container, one can mount a directory with the command

```bash
docker run -v /local/machine/path/foo:/container/path/foo CONTAINER:TAG
```

Volumes are in fact more general than this, but the general idea of persisting files
beyond the lifecycle of a single container remains. Containers can share volumes
that do not point to a folder on the host machine, for example.

### Combining containers

#### Docker compose

As stated above, many services consist of multiple containers each running a
single process. For example, a simple application might have a frontend
the user interacts with and a backend that handles reqeusts from the frontend.
A simple way to orchestrate multiple containers is to use `docker-compose`, which
is also available as `docker compose` as a subcommand of the `docker` command.
To use `docker-compose`, one writes a `docker-compose.yaml` file. This allows
one to start multiple containers with a single `docker-compose up` command
and to bring them down with a single `docker-compose down` command.

Docker compose can also be used with a single container, and we've included
a `docker-compose.yaml` file for the images we built previously. This can be
a useful way to save the starting command into source control (the git repo)
and, combined ith volumes, can be used to provide a standard way to develop
the image and use it for end to end testing.

#### Kubernetes

While base docker and docker compose commands can be used to run containers
on machines, they do not provide more complex orchestration services. For
example, if a container crashes because it runs out of memory, there is
no mechanism to automatically restart the container. This is where
[kubernetes](https://kubernetes.io/) --
often abbreviated as k8s for the 8 letters betwen the 'k' and 's' -- comes into
play. Kubernetes is an orchestration software that can be run on multiple
nodes (a cluster) and handles things such as making sure the correct number of replicas
for a set of containers is always present. It provides abstraction layers
that allow groups of containers to interact with other groups of containers
without the user having to carefully map dozens of ports correctly, for example.
We will not do more than say that this technology exists and is interacted with
via YAML files, much like docker compose, but it is quite likely that if you
create an image it will be deployed on a kubernetes cluster.
