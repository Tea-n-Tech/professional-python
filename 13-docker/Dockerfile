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
