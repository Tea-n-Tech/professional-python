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

A basic workflow from GitHub slightlu adapted looks as follows:

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
      # sucks sometimes.
      - name: Install Task
        # TODO
        run: |
          sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d

      # Install dependencies through task
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          ./bin/task setup

      # Run our linting
      - name: Lint code
        run: |
          ./bin/task lint
```

## Publishing

