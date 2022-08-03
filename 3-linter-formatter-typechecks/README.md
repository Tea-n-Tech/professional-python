# Automating Linter, Formatter and Typechecks

As easy as it is to write python so is it also easy to write
crappy python.
Fortunately, there are a lot of tools to assist you in writing
high quality code.

## Linting

A linter checks for several code quality issues and reports them
to you.
Code usually runs even if linters report issues but it will
help you avoid technical debt and advice best practices.

For linting we will use actually two linters here:

- flake9
- pylint

To add them as a development dependency but not a direct
project dependecy we first run:

`poetry add flake8 pylint --dev`

which results in the following section in our `pyproject.toml`

```toml
[tool.poetry.dev-dependencies]
pylint = "^2.14.5"
flake8 = "^5.0.3"
```

This is pretty neat as every developer will install also the
correct development tools and version from now on.
For fun, we can directly run pylint on our code:

```bash
> poetry run pylint deathstar
************* Module deathstar.laser
deathstar/laser.py:1:0: C0114: Missing module docstring (missing-module-docstring)
deathstar/laser.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)

-----------------------------------
Your code has been rated at 3.33/10
```

Ouch 😅 so little code and got a few hits right away.
You can exclude a rule as we will do in the following
but be aware that this must be done solely for good
reasons.
To disable linting for missing module docstrings we can
do this by adding a rule in a special section in the
`pyproject.toml` file:

```toml
[tool.pylint."MESSAGES CONTROL"]
disable = [
    # Disable missing module docstring since the information
    # regarding functionality is provided with more than enough
    # detail by the functions themselves
    "missing-module-docstring"
]
```

Note how easy it is to modify the linter config in the same
file as our python project, pretty compact.
Also note how I've added a comment why the rule is disabled.
Your colleagues and others will thank you for it so make it a
habit.
Running `poetry run pylint deathstar` omits the rule now:

```bash
> poetry run pylint deathstar                                               ─╯
************* Module deathstar.laser
deathstar/laser.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 6.67/10 (previous run: 3.33/10, +3.33)
```

Remember the command is a pain in the a**.
Thus storing such frequent commands is a very good idea.
We will do so in the next section, which takes a bit of a 
detour but is worth it.

## Storing Commands in a Taskfile

There are a lot of ways to store important commands for your
project.
In many cases a `Makefile` is used, but it does not support
windows (not a fan) and can be a pain in many ways.
A more modern but relatively unknown way is to use
[taskfiles](https://taskfile.dev/).
While it is for sure not broadly adapted, it is a very modern
way to store commands with a large variety of options and
has the quality of a professional tool.
You can following the website to install `task` which is provided
as a single binary.

Then create a `taskfile.yaml` in our project and fill it with
the following content:

```yaml
version: "3"

tasks:
  lint:
    desc: Lints the code and reports on issues.
    cmds:
      - python3 -m poetry run pylint deathstar
```

Now to see all available commands simply run `task` in your
project root:

```bash
> task
task: Available tasks for this project:
* lint: Lints the code and reports on issues.
```

Sweet we can see our linting task.
Now let's run it:

```bash
> task lint
sk: [lint] python3 -m poetry run pylint deathstar
************* Module deathstar.laser
deathstar/laser.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 6.67/10 (previous run: 6.67/10, +0.00)

task: Failed to run task "lint": exit status 16
```

Cool it worked 💪

## More Linting

We now use `pylint` but are still missing `flake8`.
Let's add it to our task command:

```yaml
  lint:
    desc: Lints the code and reports on issues.
    cmds:
      - |
        python3 -m poetry run flake8 deathstar \
          --show-source \
          --statistics \
          --count
      - python3 -m poetry run pylint deathstar
```

You can see we added a few flags here to configure the linter.
This is not recommended as your code editor will not use those.
Let's remove as many as we can and transfer them to our
`pyproject.toml` file:

```toml
[tool.flake8]
# I have no clue why this is 10, maybe I ought to look it up
max-complexity = 10
# We allow longer lines since 80 is quite short
max-line-length = 100
```

Nice, the linters are fine.

## Formatting

We all know it, we code happily and another person makes
changes, saves a file and it looks entirely different.
That is not professional.
We need to ensure that code is formatted consistently.
To do so, we use `black`.
Let's add it to our environment:

```bash
poetry add black --dev
```

And let's run it:

```bash
> poetry run black deathstar
All done! ✨ 🍰 ✨
2 files left unchanged.
```

Sweet, no punches here.
Let's add it to our `Taskfile.yaml`:

```yaml
  lint:
    desc: Lints the code and reports on issues.
    cmds:
      - python3 -m poetry run black --check deathstar
      - |
        python3 -m poetry run flake8 deathstar \
          --show-source \
          --statistics \
          --count
      - python3 -m poetry run pylint deathstar
```

Note how I've added the `--check` flag to `black` as by default
it will format your code but during linting we only want to check
it.
Let's configure `black` further in our `pyproject.toml` file:

```toml
[tool.black]
line-length=100
```

Now also our line length is consistent with the other linters.
Note how our linting command grows in complexity but in a healthy
way.

## Typechecks

Last but not least, we need to ensure that our code is typechecked.
Python is notoriously known for using dynamic typing.
That is one reason why it is so popular.
In a professional environment this poses an issue as in a static
language a lot of bugs can already be spotted during compilation.
To improve our code health let's add a typechecker.

We will use `mypy` here which is the most popular one.
There are other good ones too such as for example `pyre`
so don't stay stiff on this.
Important, any typechecker struggles if your code depends on
certain manipulations such as generating code at runtime.
In such a case it can be very reasonable not to use a typechecker.

Let's add it to our environment:

```bash
poetry add mypy --dev
```

And run it too:

```bash
> poetry run mypy deathstar
Success: no issues found in 2 source files
```

Great! As you know the drill, let's add it to our `Taskfile.yaml`:

```yaml
  lint:
    desc: Lints the code and reports on issues.
    cmds:
      - python3 -m poetry run mypy deathstar
      - |
        python3 -m poetry run flake8 deathstar \
          --show-source \
          --statistics \
          --count
      - python3 -m poetry run pylint deathstar
      - python3 -m mypy deathstar
```

We put the typechecker last as it requires a lot of time.

## Installation Command

A little appendix here, let's add a command to our `Taskfile.yaml`
to simplify installation of the dependencies:

```yaml
  install:
    desc: Installs the dependencies.
    cmds:
      - poetry install
```

Other developers or automatization pipelines can use this command
and we don't have to remember it.
See how we channel most complexity into certain places:

- `Taskfile.yaml` for commands
- `pyproject.toml` for configuration

If we or others ever search for any of both they know where to find
it and if you use comments, they also know what stuff is what
and why it was done that way.
