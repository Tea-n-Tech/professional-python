
# 📦 Package Management

This tutorial explains how to create a python package which can be uploaded to
[pypi].

[pypi]: https://pypi.org/

## Package Managers

There are multiple ways how to create and manage python packages.
It is important to know that this topic is not just about deploying a package.
It is also about managing the development environment.

Why are they closely interconnected?

Because during development we want to have:

- A clean and identical development environment
  for every developer
- Everyone installing the package to have the same dependencies
  so debugging is easier
- Ensure automated testing also uses the same environment
- Build and upload the package with well-defined dependencies

Consequently, the development environment and package management are closely
connected.
Environments and packages can be managed entirely or partially with the
following solutions:

- [conda]
- [pipenv]
- [poetry]
- [venv]
- ...

They all were created to manage certain aspects of a package and some can do
more than others and some also rely on each other.
To avoid a lengthy factual discussion, here is a direct and brief advice:

- By default use [poetry]
- Use [conda] if your package also depends on certain binaries (e.g. Intel MKL)

[conda]: https://docs.conda.io/en/latest/
[pipenv]: https://pipenv.pypa.io/en/latest/
[poetry]: https://python-poetry.org/
[venv]: https://docs.python.org/3/tutorial/venv.html

## Poetry

### Why is Poetry a default choice?

- Modern and easy to use
- Creates automatically a virtual environment for the repository directory
- Has a built-in dependency installer and updater
- Provides a package lockfile to ensure all users have the same
  dependencies installed
- Can build and upload the package to pypi
- It is fast enough to be used as a development environment
  (some can be slow)

This guide will focus on poetry alone from now as it covers the majority of
use-cases.

### Getting started

Run `poetry init` in the root directory of your project and answer
all questions.
Don't worry you can modify anything later.
This will create a `pyproject.toml`.
This famous file configures almost your entire project later on
including linting as you will see.
We will call the new package `deathstar`.

### First code

After running `poetry init`, we will add a directory called
`deathstar` containing a legendary `__init__.py` file to mark
it as a package.
Beside it, we create another file `deathstar/laser.py` containing
the function:

```python
def fire(planet: str):
    print(f"Firing laser at '{planet}'")
```

In the following we want to expose this function as our libraries
functionality.

### Adding packages

Since the output is a boring print statement, we will add the
package `rich` which can print text with colors in terminals.
To do so we run:

```python
poetry add rich
```

which yields the output

```bash
Creating virtualenv deathstar-nPBsZxp8-py3.9 in /home/codie/.cache/pypoetry/virtualenvs
Using version ^12.5.1 for rich

Updating dependencies
Resolving dependencies... (0.8s)

Writing lock file

Package operations: 3 installs, 0 updates, 0 removals

  • Installing commonmark (0.9.1)
  • Installing pygments (2.12.0)
  • Installing rich (12.5.1)

```

Poetry created a virtual environment for us automatically since there
was none yet (cool!) and installed `rich`.
The dependency is now also in our `pyproject.toml` file:

```toml
[tool.poetry]
name = "deathstar"
version = "0.1.0"
description = "This python package allows running the deathstar"
authors = ["Lord Vader <darth.vader@galactic-empire.star>"]
license = "MIT"

[tool.poetry.dependencies]
python = "^3.7"
rich = "^12.5.1"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

Now we can use rich to print a colored text:

```python
import rich


def fire(planet: str):
    rich.print(f"💥 Firing laster at [red]{planet}[/red]")
```

### Manual Testing

Okay we got our code set up but how to manually run the code?
If you simply do the following it will fail:

```bash
$ python
Python 3.9.12 (main, Apr  5 2022, 06:56:58) 
[GCC 7.5.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import deathstar
>>> deathstar.laser.fire("alderaan")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'deathstar' has no attribute 'laser'
>>> from deathstar import laser
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/codie/programming/python/professional-python/1-package-management/deathstar/laser.py", line 1, in <module>
    import rich
ModuleNotFoundError: No module named 'rich'
```

This is because your main python environment does not have rich installed.
To fix this we need to run the python of the virtual environment
which poetry created for us through:

```bash
$ poetry run python
Python 3.9.12 (main, Apr  5 2022, 06:56:58) 
[GCC 7.5.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from deathstar import laser
>>> laser.fire("alderaan")
💥 Firing laster at alderaan
>>> exit()
```

Everything that you want to run in the virtual environment requires
`poetry run`.
To avoid typing, you can also use `poetry shell` to get a shell in the
virtual environment and then simply run e.g. `python`.

### Development Dependencies

Just as a brief note here, in the `pyproject.toml` file we have a
`[tool.poetry.dev-dependencies]` section.
In this section we denote packages which we need for development
but not for running the actual code such as `black` for formatting.
This topic will be covered in another session.

### Upload to PyPi

Now that we have a package, how do we distribute it?
Obviously we ought to upload it to pypi from where users can
install it by running `python -m pip install deathstar`.

First we build our package with:

```bash
$ poetry build
Building deathstar (0.1.0)
  - Building sdist
  - Built deathstar-0.1.0.tar.gz
  - Building wheel
  - Built deathstar-0.1.0-py3-none-any.whl
```

The python wheel (.whl) can be found in a folder `dist`
including the source distribution (.tar.gz).
These files need to be uploaded next.
For the sake of professional development first upload to
[test-pypi] to test everything.
Assuming you already have an account, run the following
commands:

```bash
# Register test pypi
poetry config repositories.test-pypi https://test.pypi.org/legacy/

# Set API token from user settings
poetry config pypi-token.test-pypi  pypi-XXXXXXXXXXXXXXX

# Upload the package
poetry publish --build -r test-pypi
```

For a production release set the token for the main pypi instance
and remove the test-pypi reference.

```bash
poetry config pypi-token.pypi pypi-XXXXXXXX
poetry publish --build
```

Congratulations 🥳 your package manager is all set up.

[test-pypi]: https://test.pypi.org/
