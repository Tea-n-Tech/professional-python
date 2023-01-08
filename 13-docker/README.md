
# Docker

Nowadays docker is a mandatory skill for any kind of programming job.
Docker is a toolchain to build containerized applications and also run them
in a dedicated environment.

## Disclaimer

A lot of things will be a bit vague in the following sections.
Fact is, running containers does not work everywhere the same.
The runtime varies depending on the operating system and configuration.
Thus it is hard to establish a general truth in a lot of statements.
Main focus will be here docker on Linux.

## Containerization

The rough idea of docker is as follows:

![Docker creation meme](./assets/docker-meme.jpg)

Often an application requires additional things.
For example python applications require a system with python including all
required dependencies installed.
But beyond that, some python libraries are written in C/C++ or Fortran and
require additional runtime libraries such as the Intel Math Kernel Library
(MKL).
And even if your target system has those libraries, it might not have them in
the right version and things get funny.
You get the idea why shipping an application with an entire environment makes
a lot of sense for anything more complex.
Beyond environments, it is also important to isolate applications.
If you run 20 applications on a server next to each other they might at best
interfere with each other and at worst hack each other due to CVEs.
Also their dependencies will very likely conflict at these numbers.
Thus isolation is also a really important reason for containers.
Note there are other solutions than containerization (see [WASM] for example).

[WASM]: https://webassembly.org/

## How it works

Docker does roughly two things:

- Building a docker image
- Running the docker image as a container

There is more and of course in detail things are more complicated but that is a
topic for another time.
A docker image can be imagined like an operating system like image e.g. Ubuntu
on which you install your dependencies and application.
This is done in a `Dockerfile` which is basically just an installation procedure
written down with some additional features.
After building the image (more about that later), it can be run or stored
externally for e.g. servers to pull them and run them themselves.

> Docker in its essence runs a dedicated application as a process in an
> isolated filesystem, the docker image, with limited restrictions such as
> memory, networking or CPU.

The image still runs on the original system as a dedicated process, so it is not
a dedicated operating system running but just the environment.
This is the major difference to VMs by the way and means you cannot run a
windows image on linux and vice versa although there are container runtimes scheduling containers in a VM which makes it possible.

## Containerize all the things

Here, we want to containerize our API server.
This is pretty much standard procedure so in case you search for a job to build
APIs you can expect having to containerize them.
To get started, [install docker][install-docker].
Next we need a `Dockerfile`.
Check out the following content and go through it:

[install-docker]: https://docs.docker.com/engine/

```dockerfile
# We use the python base image as it already has what we need.
# Always in a work environment pin versions, otherwise things might break
# overnight in case a new docker image rolls out due to incompatabilities.
# Also we name it builder as you will see later.
FROM python:3.11 AS builder

# We create a working directory in the Dockerfile and automatically change
# directory in it.
WORKDIR /app

# Install poetry coz we need it
RUN python -m pip install poetry

# Install task to make our life easier
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" \
    -- -d -b /bin
COPY Taskfile.yaml .

# First we install all dependencies separately. Why? Because docker caches each
# step in a layer and does not rerun it if anything changes. If we just copy all
# at once we have to install the dependencies all the time again just because
# we changed a single line in a single source file.
COPY pyproject.toml .
COPY poetry.lock .
RUN task install

# Now copy the source code and build the python wheel
COPY deathstar deathstar
RUN task build

# This is a neat trick. Building often creates bloat which we don't need.
# For example poetry creates a venv besides other things. To discard it and
# have a minimal image we can just take what we need from the previous builder
# image and copy it to a new, clean image. This is good practice.
FROM python:3.11

# Go into our app dir again
WORKDIR /app

# Now copy our final wheel from the builder here and install it cleanly.
COPY --from=builder /app/dist/*.whl .
RUN python -m pip install *.whl

ENTRYPOINT [ "deathstar", "api" ]
```

Looks fairly easy, copy around things and run commands.
An important topic to keep in mind is to mind the order since docker caches
layers where nothing happens.
Now how to we build the container?
Simply by running:

```console
$ docker build -f Dockerfile -t ghcr.io/deathstar:latest .
```

Where `-f` denotes the file (optional), `-t` tags the docker image with a name
and `.` denotes the "context" aka working directory.
The name starts with the registry url, which is the github container registry
here (ghcr), followed by the repo owner and name.
After `:` one does specify a version.
As an example we simply go with `latest` although we correct this in the CD
pipeline.
Store this command in your `Taskfile.yaml` to not forget it:

```yaml
env:
  DOCKER_REGISTRY: ghcr.io
  DOCKER_OWNER: tea-n-tech
  DOCKER_IMAGE_NAME: deathstar
  DOCKER_IMAGE_VERSION: latest

# ...

  docker:build:
    desc: Build the docker image
    cmds:
      - >
        docker build
        -f Dockerfile
        -t "${DOCKER_REGISTRY}/${DOCKER_OWNER}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION}"
        .
```

Okay so we can build the image now, but how do we run it?
Let's add another command to our taskfile:

```yaml
  docker:run:
    desc: Run the docker image api
    cmds:
      - >
        docker run
        -p 8080:8080
        "${DOCKER_REGISTRY}/${DOCKER_OWNER}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION}"
```

Try it and run `task docker:run` in the console.
It will start the API server through the deathstar CLI in the docker image.
With `-p 8080:8080` we forward the docker image port 8080 to the operating
system port 8080.
This is allows us to test the API outside of the container.

## Publish

Lastly, we need to upload the image somewhere so that we or others can use it.
Companies often have custom docker registries with access restrictions.
In the public domain, most people go with [Docker Hub] although for GitHub
repositories, the GitHub Container Registry (GHCR) is a very good choice.
We will go with the ghcr here as depicted above.

First we need to log into the GHCR:

```console
docker login ghcr.io -u your_username
```

Use as password a GitHub token with the read/write access to "packages".
Once login was a success, we can upload the image with the following task
command:

```yaml
  docker:upload:
    desc: Upload the docker image to GitHub
    cmds:
      - >
        docker push
        "${DOCKER_REGISTRY}/${DOCKER_OWNER}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION}"
```

Once you start the upload, the individual layers are pushed to the remote.
It looks roughly as follows during the upload:

```console
The push refers to repository [ghcr.io/tea-n-tech/deathstar]
d6893fa65e99: Pushed 
f30f84cdf34c: Pushed 
f6438de1ca18: Pushed 
8b0860f70229: Pushed 
1741b53163b6: Pushed 
636a428ce0f7: Pushed 
248397b6b856: Pushed 
fa1175420e6f: Pushed 
bb2453e12947: Pushed 
7354e83da007: Pushed 
c284f546974c: Pushed 
4efcd4003c84: Pushed 
latest: digest: sha256:0180a6159bfc8d1b45ac502021ebf11c7dd577aa022c942ae14ba09e79d17a67 size: 2844
```

This can take a while as this image is quite heavy.
Once you are done, congratulations to your first, manual upload.
But we want to automate it so that this happens automatically during a release.
Therefore we add another job to our
`.github/workflows/python-lint-test-upload.yml` file.

```yaml
  # JOB
  # Now we upload our docker image. The docker image
  # is uploaded to the repositories container registry.
  docker:
    name: Publish docker image

    needs: [publish]
    if: startsWith(github.ref, 'refs/tags/')

    env:
      REGISTRY: ghcr.io
      IMAGE_OWNER: tea-n-tech
      IMAGE_NAME: ${{ github.repository }}

    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Log in to the Container registry
        uses: docker/login-action@f054a8b539a109f9f41c372932f1ae047eff08c9
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@98669ae865ea3cffbcbaa878cf57c20bbf1c6c38
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_OWNER }}/${{ env.IMAGE_NAME }}

      - name: Build and push Docker image
        uses: docker/build-push-action@ad44023a93711e3deb337508980b4b5e9bcdc5dc
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

Take attention of especially the metadata extraction action.
Giving the image the correct version can be done from git information such as
tags which is exactly what the action does.
You could do all of that of course manually.

This is roughly it 😌
You can bundle your application now in a docker image and upload it to a
specific location.
Other applications such as Kubernetes then can pull the image and run it.

[Docker Hub]: https://hub.docker.com/
