# Unit-Testing

There is a large variety of ways to test your code:

- Unit Testing
- Integration Testing
- System Testing
- Performance Testing
- Fuzzy Testing
- ...

Here we will focus on the most basic type: unit-testing.
Unit-testing is the least required type of test which is always expected to
be present if it is not just a throwaway script.

## Framework

Unit tests literally test a unit, thus usually a function.
For that a lot of frameworks exist but we will go with the most common one:
`pytest`.
The alternative would be using the standard python library `unittest`
but `pytest` has a more modern flavour 🧁

Let's install pytest:

```bash
poetry add --dev pytest
```

Nice, lets add a test ... but where.
This is an ancient topic of discord ⚔️
If you want to do it cleanly you can put the tests in a separate `test`
directory.
Why?
Because then when you ship your package you don't ship the tests.
Nonetheless this approach often results in duplicating the folder structure
and duplication always has the burden of keeping things in sync.
That is why a lot of people put the tests next to their source files.
While it is rationally not so clean, it gives it a very nice taste of
cohesion since things belonging together are close to each other.
There are also tricks to exclude those test files from shipping.
Play with both variants if you like.
Here we will assume putting the unit tests next to the source files for
simplicity.
No one will give you trouble as long as you can give good reasons.

## First Test

Let's add the file `deathstar/test_laser.py` pewpew ✨
Now, most commonly people structure their tests in a class and we will follow
this best practice.
Then we add a function starting with `test_`.

```py
from .laser import fire


class TestLaser:
    def test_fire_success(self):
        fire("Alderaan")
```

Let's run the tests:

```bash
> poetry run pytest
============================= test session starts ==============================
platform linux -- Python 3.9.12, pytest-7.1.3, pluggy-1.0.0
rootdir: /home/codie/programming/python/professional-python/7-unit-testing
collected 1 item                                                               

deathstar/test_laser.py .                                                [100%]

============================== 1 passed in 0.05s ===============================

```

Nice it works!
Let's quickly add this command to our `Taskfile.yaml`:

```yaml
  test:
    desc: Runs tests on the code
    cmds:
      - poetry run pytest
```

But what do we test?
We just test that this routine does not throw.
That is not really a lot, for example we don't test if it really prints.
But how do we do that?

## Side-Effects 💀

If you run a function repeatedly, given the same input you would expect the
same output.
This is the case if there are no side-effects present.
Side-effects are things going on inside a function which can possibly cause a
different output or even failure.
Typical side-effects are interacting with the filesystem, printing output,
sending requests across the network etc.

### Dealing with Side-Effects

It is important to understand that Python is really generous in allowing you
to test these things 😯
In other languages you usually use interfaces to deal with these things which
introduces additional complexity.
Python on the other hand says: do your thing in the function and we can replace
the real function calls during testing with so-called mocks.
This can be done since Python is a dynamic language.

### Mocking

In our function `fire` we do system IO which is a side-effect.
We don't really know if stuff was printed or not.
Let's use a mock to replace the side-effect and verify that it was used
correctly.

```py
from .laser import fire
from unittest import mock


class TestLaser:
    @mock.patch("deathstar.laser.rich", autospec=True)
    def test_fire_success(self, rich_mock):

        # let mock print return None
        rich_mock.print.return_value = None

        fire("Alderaan")

        assert rich_mock.print.called
        rich_mock.print.assert_called_once_with(f"💥 Firing laster at [red]Alderaan[/red]")
```

That is pretty neat.
Be mindful how in the top we pinpointed to the import within the package.
We did not patch `rich` but `deathstar.laser.rich`!
To find out more what `patch` can do see the [unittest docs][unittest-patch].

[unittest-patch]: https://docs.python.org/3/library/unittest.mock.html#

IMPORTANT!

- In unit-tests you should avoid testing functions deeper down in the callstack.
  This can lead to an enormous increase in scenarios.
  Feel free to patch not only function calls, but also more complex functions
  which you are calling.
- In the last line we basically check the entire implementation.
  Avoid this if possible.
  We don't want a test to break just because someone changes the color.
  That would be too detailed.
  Checking if it was called would suffice in this case.

There are other ways to use mocks.
There is also [pytest monkeypatch][pytest-monkeypatch] which you could also use.
I myself always found it much less practicable than `unittest.mock`.

[pytest-monkeypatch]: https://docs.pytest.org/en/latest/how-to/monkeypatch.html#

## Continuous Integration

What would be our continuous integration pipeline without unittests?!
Let's add it so that we can check not only our code quality with linting
but also if it works.

```yaml
# jobs.test.steps:
      - name: Test code
        run: |
          ./bin/task test
```

## Pre-Commit Hook

Also don't forget to add the tests to the pre-commit hook in
`.pre-commit-config.yaml`.

```yaml
repos:
  - repo: local
    hooks:
      - id: python-linting
        name: python-linting
        entry: task lint
        language: system
        types: [python]

      - id: python-testing
        name: python-testing
        entry: task test
        language: system
        types: [python]
```

Congratulations!
You know the essentials and basics of unit-tests now.
