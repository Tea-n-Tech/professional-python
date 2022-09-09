# Continuous Integration (CI) Pipelines

Continuous Integration (CI) and Continuous Deployment (CD) are an absolute
must have for any professional project.
The motivation is quite simple, you can run your linting and tests locally,
yet you might forget to do so.
To ensure a high code quality, every change pushed to your repository needs
to be checked automatically.
This can be done with CI pipelines which simply run your checks.
CD is the counterpart which uploads the code with every new release or even
deploys it in case of a web service such as an API.

## GitHub Actions

Since our code is already hosted on GitHub, we can use
[GitHub actions][gh-actions].
If you want to learn the basics or learn more about it
read the docs since this is what professionals do.
To create a workflow we just need to define it in a
workflow file with a specific yaml format.
GitHub will then on every push spawn a virtual machine and
execute the workflow.
In a workflow, you can do anything you like, from testing
code to sending a message to your husband or wife.

[gh-actions]: https://docs.github.com/en/actions

## Workflow File

ℹ️ Start simple with a default workflow on GitHub and
incorporate improvements step by step.

First create the folders `.github/workflows` in your project.
Then create a workflow file called `python-lint-test-upload.yml` or choose
any name you like, it does not matter.

Be aware of the following: This tutorial will do fancy stuff.
We recommend to start with a plain workflow from GitHub
(they have defaults) and then incrementally improve it.
The reason is a lot of steps here are crafted from pain
to make things faster or simplify debugging.
If you never had pain in the first place we recommend you
to get some first so that you truly get a feeling for
why it is reasonable.

## Basic Setup and Testing

A basic workflow from GitHub slightly adapted looks as follows:

```yaml
# Workflow name displayed
name: Python package

# You can control when to trigger this workflow. You can
# generally trigger on any push or pull request as shown
# here but also other triggers based on time or specific
# files or other events is possible.
on: [push, pull_request]

# Jobs to execute
jobs:
  # Job
  # This job is called "build" which is a custom name. You may
  # choose a different one. 
  build:
    # We run our workflow on ubuntu linux here.
    # It is a popular system and stuff usually works well on it.
    runs-on: ubuntu-latest

    # This is a bit specific but it offers to run the tests
    # for multiple python versions. After all we want to test
    # usually not only the latest but also least supported
    # version.
    strategy:
      # If either the tests for 3.7 or 3.10 fail all workflows
      # are terminated to safe computing resources.
      fail-fast: true
      # Test matrix consists of two python versions. Usually
      # latest and lowest supported are enough.
      matrix:
        python-version: ["3.7" , "3.10"]

    # Define workflow steps. Here the Party begins.
    steps:
      # This is an action from the action store.
      # It uses git to clone and checkout our code from GitHub.
      # Otherwise we would have to do it manually.
    - uses: actions/checkout@v3

      # This action installs python. Workflows have variables such as the python
      # version from the matrix section. We use this variable to install the
      # respective version here.
      # As you can see actions may have inputs since they are basically something
      # like a function. Inputs are denoted by 'with'.
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}

      # We install task here since all our commands are already
      # nicely available through it. Two things are important!
      # We need to fix the version instead of using latest and
      # we need to verify the SHA hash of the version to make
      # sure we got the right binary. Yes professional life
      # sucks sometimes but breaking CI/CD sucks more.
      - name: Install Task
        # TODO
        run: |
          sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d

      # Install pip as package manager just to be safe
      - name: Install and upgrade pip and poetry
        run: |
          python -m pip install --upgrade pip poetry

      # Install dependencies through task
      - name: Install Dependencies
        run: |
          ./bin/task install

      # Run our linting
      - name: Lint code
        run: |
          ./bin/task lint
```

## Improvements

This section will cover multiple improvements you can make
over time.
Be aware you can spend an eternity optimizing CI/CD so don't
overdo it.
Simply focus on pain points such as long runtimes.
A good developer knows how much to do by feeling and not
strict guidelines.

### Caching .venv

If you run the pipeline multiple times you will recognize that
`poetry install` will take very long which sucks for multiple
reasons.
To avoid this we can cache our poetry venv.
First we need to tell poetry not to install the venv in our home
directory under `$HOME/.cache/pypoetry/virtualenvs` but to
create it within our repo directory.
We can do this by adding a flat to our install command in our
Taskfile:

```yaml
# ...
  install:
    desc: Installs the dependencies.
    cmds:
      - poetry install --no-root
# ...
```

Now in the workflow file, BEFORE running `task install` add the
following code:

```yaml
      # Load our cached dependencies to speed things up.
      # You will get more motivation for this extra stuff
      # one you waited minutes.
      - name: Load cached venv
        id: cached-poetry-dependencies
        uses: actions/cache@v2
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ hashFiles('**/poetry.lock') }}
```

And congratulations your pipelines should be much faster now 🏎️

### Saving Artefacts

Debugging pipelines can be very painful and is especially in GitHub
Actions a big pain point.
To help with this you can actually store arbitrary artefacts with
your workflow run.
Artefacts simply means store any file you like.
This can be logfiles, binaries or libraries.
Once this odd error pops up, we can directly inspect the artefacts
without having to reproduce the error.

To store artefacts, we can simply use an action.
Here we will store the build packages in the `dist` folder
after running `task build` (will be done during publishing
as shown below).

```yaml
      # Not required but this saves the distribution files
      # with the package upload. You can also do this with
      # e.g. log files etc. Can make debugging easier to have
      # the real code available just to be sure.
      - name: Save packages as artifacts
        uses: actions/upload-artifact@v2
        with:
          name: dist
          path: dist
          if-no-files-found: error
```

## Test Publishing

Now that we check our code, we also need to publish it.
The most common and public place to publish python libraries
is [PyPi].
Simply create an account and a token and you are ready to publish
... almost.
You also need an account on [Test PyPi][test-pypi] since we want
to test the upload itself and the installation.

[pypi]: https://pypi.org/
[test-pypi]: https://test.pypi.org/

First create a new `job` in the workflow file as shown below:

```yaml
  # JOB
  # This job publishes the package to test-pipy.
  # You don't want to upload to pipy itself right away
  # without a test. Helps during development.
  test-publish:
    # Will run after the job 'tests'
    needs: [tests]

    # Important, this job will run only if we tag the source
    # code with `git tag -a X.X.X`.
    if: startsWith(github.ref, 'refs/tags/')
    runs-on: ubuntu-latest

    # Jobs can have outputs for reuse. We want to reuse
    # the version of the package.
    outputs:
      version: ${{ steps.extract_version.outputs.version }}

    steps:
      # Check out source code with this action again. You
      # need to do this in every job.
      - uses: actions/checkout@v2

      # This is something more advanced but a step can have
      # outputs which can be used in other steps.
      # We extract from the toml file the version here
      # and set it in a very very odd syntax as the output.
      - name: Remember version
        id: extract_version
        run: |
          VERSION=$(cat pyproject.toml | grep -oE -m 1 "version = \"(.*)\"" | cut -f2 -d '"')
          echo "Version: $VERSION"
          echo "::set-output name=version::$VERSION"

      # For publishing just pick a python version
      - name: Set up Python 3.10
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"

      # Installing task ... again
      - name: Install Task
        run: |
          sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d

      # Load our cached dependencies to speed things up.
      # You will get more motivation for this extra stuff
      # one you waited minutes.
      - name: Load cached venv
        id: cached-poetry-dependencies
        uses: actions/cache@v2
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ hashFiles('**/poetry.lock') }}

      # Install dependencies ... again
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip poetry
          ./bin/task install

      # What the description says
      - name: Build packages for release
        run: |
          ./bin/task build

      # Here we actually upload to pipy. Poetry can do that on
      # its own BUT we use the classic twine here.
      # Why? Couse twine can skip existing which avoids any tries
      # to upload multiple times.
      - name: Publish distribution to Test PyPI
        env:
          TWINE_REPOSITORY_URL: https://test.pypi.org/legacy/
          TWINE_USERNAME: __token__
          TWINE_NON_INTERACTIVE: 1
          TWINE_PASSWORD: ${{ secrets.TEST_PYPI_API_TOKEN }}
        run: poetry run twine upload --skip-existing --verbose 'dist/*'

```

Wow that was a lot of input.
Now you know why caching `.venv` is important, otherwise you need to
reinstall stuff again and again for every job (duh).

### Package Building

The command `task build` is still missing in our `Taskfile.yaml`.
Simply add it as follows:

```yaml
  build:
    desc: Builds the puthon package
    cmds:
      - poetry build
```

### Twine

Also in contrast to the initial example we use `twine` instead of
`poetry publish`.
This is due to the grateful existance of the `--skip-existing`.
If multiple jobs try to upload (can happen easily with test
matrices), then only one upload will succeed and all others are
ignored.
It is a nice old and lazy trick.
`poetry publish` on the other hand will fail.
This feature is still under discussion for poetry.
Yes this is a taste of professional development too.
These nuances make the quality if CI/CD much better.

Don't forget to install twine with poetry by the way:

```bash
poetry add --dev twine
```

### Secrets

A very important line is

```yaml
       TWINE_PASSWORD: ${{ secrets.TEST_PYPI_API_TOKEN }}
```

setting the pypi test password as an environment variable.
This is a [GitHub secret][gh-secret], which can be set up for
repos and orgs.
The cool thing is, that the secret can be used by other developers
without having to know it which is the main purpose.
Secrets can also be restricted to certain branches etc to
make it even more secure, but this would be a bit much here.
As I said before, CI/CD is an endless pit of optimizations.
If you like more stuff like this consider becoming a DevOps
engineer.

[gh-secret]: https://docs.github.com/en/actions/security-guides/encrypted-secrets

### Test Installation

Normally developers now just upload the package to the real
pypi or an artifactory storage of their choice.
Here we will turn an extra round by trying to install the test
release first.
This care came from yet another painly mistake I had where
dependencies broke my package due to conflicts or errors.
Here is the `job` for the test installation:

```yaml
  # JOB
  # Yeah you thought we must be done at some point but you
  # are wrong. Being professional is about a lot of extra
  # rounds and not coding. Now we test if our package
  # installation from test-pypi works. This is especially
  # helpful if you have C-dependencies.
  # It might look quite haunting to do this but I had
  # dependencies break compatabilities etc in the past
  # so this care comes from pain and suffering.
  test-install:
    # Of course run after test publish since we need it.
    needs: [test-publish]

    # Tag filter just to be safe.
    if: startsWith(github.ref, 'refs/tags/')

    # Stick with ubuntu
    runs-on: ubuntu-latest

    # Use the version from the previous job to install
    # the correct package version. We could simply go for latest
    # but in case of an unrecognized failure ... which happened
    # you will simply install an old version here.
    env:
      VERSION: ${{ needs.test-publish.outputs.version }}

    steps:
      # Install python (be aware NO checkout action)
      - name: Set up Python 3.10
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"

      # Check if it installs without errors
      - name: Install package
        run: |
          python -m pip install \
            --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple \
            deathstar=="$VERSION"
```

Note how we set `VERSION` with the version output from the
previous job through `${{ needs.test-publish.outputs.version }}`.

### Publishing

Now we are finally ready to publish our package:

```yaml
  # JOB
  # Finally publish the code to pypi
  publish:
    # You should know by now what all of this does ...
    needs: [test-install]
    if: startsWith(github.ref, 'refs/tags/')
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python 3.10
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"

      - name: Install Task
        run: |
          sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d
      - name: Load cached venv
        id: cached-poetry-dependencies
        uses: actions/cache@v2
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ hashFiles('**/poetry.lock') }}

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip poetry
          ./bin/task install

      - name: Build packages for release
        run: |
          ./bin/task build

      # Not required but this saves the distribution files
      # with the package upload. You can also do this with
      # e.g. log files etc. Can make debugging easier to have
      # the real code available just to be sure.
      - name: Save packages as artifacts
        uses: actions/upload-artifact@v2
        with:
          name: dist
          path: dist
          if-no-files-found: error

      # Basically the same as for test-pypi but we upload here
      # to pypi itself.
      - name: Publish distribution to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_NON_INTERACTIVE: 1
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: poetry run twine upload --skip-existing --verbose 'dist/*'
```

Phew that was a long ride, time for a tea 🍵😌
