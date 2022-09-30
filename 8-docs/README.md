# Documentation

Code without docs is like medicine without instructions.
You will eventually find out into which opening to put how much medicine
but it goes much faster with at least some rough instructions.
Depending for whom your code is meant for, certain types of docs make
sense.

## Doc Types

Consider to use the following topics for your docs:

- User Documentation
  - General introduction
  - Quick-start and installation guide
  - Architectural decisions (ADRs)
- Technical Documentation
  - Architecture guide
  - Source code map
  - Contribution guide
  - FAQ
  - [arc42]

If your project is in its early stages, not all parts will be necessary.
With increasing progress though you should add piece by piece more information
about your code.
Always think first is there any need by someone to have this piece of
documentation.
Otherwise you will write a book about things which in the end no one ever
needed and waste a lot of time.

### Architecture Decision Records (ADRs)

Quite unknown but very important are usually ADRs.
They document major architecture decision such as why you chose a library or
why you went with a specific solution pattern.
When should you raise an ADR?
If something is unclear and you or the team investigate which route to go.
In the end you can channel that knowledge into a compact ADR which is very
fruitful knowledge for anyone reading your docs.

### Souce Code Map

Many documentation frameworks offer the capabiity to collect all docstrings from
your public functions and classes and display them nicely.
This is a must for at least the public interface of a library.
If you don't want to spend too much time on this in the beginning you can also
simply write a small guide displaying the interface functions and their usage.
In case the interface gets bigger you can still migrate to a source code map.

### Frequently Asked Questions (FAQ)

From time to time, users will ask questions.
If they do so, consider collecting them in an FAQ.
This will save you a lot of time and also give the users insights into the
software.

### Doing it thoroughly - arc42

If you have the need to create a detailed documention for your software, then
consider using an architecture guide.
There are many guides for documenting your software.
A very compact but also quite complete one is [arc42].
I highly recommend arc42 since it depicts very cleanly how to document a
software including deployment.
Be aware this takes time and effort.
And also don't just follow any guide such as arc42 rigidly.
Think about what makes sense to document and leave out the parts where no
stakeholders have any benefit of.

[arc42]: https://arc42.org/overview

## How to document code?

Now we know what to document but not how.
In Python it usually comes down to three solutions.

- [Markdown]
- [Sphinx]
- [Mkdocs]

In the beginning, start with pure markdown.
It is dirt cheap, gets nicely displayed in repos and costs you nothing in
effort.
After you collect a few files, consider migrating to either Sphinx or Mkdocs.
Both are capable and have a lot of plugins so there is no clear winner.
Migrating to Mkdocs is a bit easier since it uses markdown for source files
whereas Sphinx goes for reStructured Text (rst).
In this course we will go with Mkdocs but feel free to make other choices.

[markdown]: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
[mkdocs]: https://www.mkdocs.org/
[sphinx]: https://www.sphinx-doc.org/en/master/

### Basic Setup

As usual add mkdocs as dev dependency:

```bash
poetry add --dev mkdocs mkdocs-material 
```

⚠️ At the time of writing, there is a dependency conflict between `mdbom` and
`mkdocs-material` regarding Jinja2.
I raised the issue [here][issue-mdbom].
Yes such situations are also part of the professional life.

[issue-mdbom]: https://github.com/HaRo87/mdbom/issues/34

We use `mkdocs-material` which uses the very beautiful [Material Theme][mui].
You can now init mkdocs:

[mui]: https://mui.com/

```bash
> poetry run mkdocs new .
INFO     -  Writing config file: ./mkdocs.yml
INFO     -  Writing initial docs: ./docs/index.md
```

The `mkdocs.yml` file is just the general config file whereas `docs/index.md`
represents your documentation root.
Of course we will change a lot of things now.
Edit the `mkdocs.yml` as follows:

```yaml
# Some general page information
site_name: Deathstar 💥
site_url: https://Tea-n-Tech.github.io/deathstar/

# We want to use the material theme
theme:
  name: material

# The pages which you want to add
nav:
  - Home: index.md
  - Quick-Start: quick_start.md
  - FAQ: faq.md
```

Now let's run mkdocs and look at the results:

```bash
poetry run mkdocs serve
```

And bam, we already got really nice docs.
Before we tune this further, let's add automatic deployment.
First we add additional commands to our `Taskfile.yml` so we don't have to
remember anything:

```yaml
# ...

  docs-serve:
    desc: Serve the documentation locally
    cmds:
      - poetry run mkdocs serve

  docs-publish:
    desc: Publish the documentation to gh-pages
    cmds:
      - poetry run gh-deploy --force
```

Now add another step after publishing your package to the
`.github/workflows/python-lint-test-upload.yml` file.

```yaml
# ...

      # Basically the same as for test-pypi but we upload here
      # to pypi itself.
      - name: Publish distribution to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_NON_INTERACTIVE: 1
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: poetry run twine upload --skip-existing --verbose 'dist/*'

      # Upload documentation to gh-pages
      - name: Upload docs to the gh-pages branch
        run: poetry run mkdocs gh-deploy --force
```

Okay cool ... but where does this actually deploy to?
GitHub has a special branch called `gh-pages`.
This branch is THE branch for uploading static pages belonging to your
repo.
The branch DOES NOT contain the source code.
It is a so called orphan branch, meaning it has no connection to the coding
branches as it is just for docs.
The site data contains a file `index.html` which will be rendered automatically
by GitHub, so cool 😎

### Source Map

In case we offer a library such as here, we need to document the public
function interface.
Therefor we need an additional package [`mkdocstrings[python]`][mkdocstrings].
The feature flag `python` indicates that we want to document python code.
Okay let's install the plugin:

```python
poetry add --dev mkdocstrings[python]
```

Now we register the plugin including the search plugin (should be installed by)
default in the `mkdocs.yml`.

```yaml
# Some general page information
site_name: Deathstar 💥
site_url: https://Tea-n-Tech.github.io/deathstar/

# We want to use the material theme
theme:
  name: material

# The pages which you want to add
nav:
  - Home: index.md
  - Quick-Start: quick_start.md
  - FAQ: faq.md
  - Source Code: source_code.md

plugins:
  - search
  - mkdocstrings
```

As shown above we need to create a new source file `source_code.md` on which we
document our public function interface.
Let's document our function `laser` in it:

```md
# Source Code

::: deathstar.laser
```

This is enough, now you should see really nicely documented code when running
`task docs-serve` 💘

As a note, we adapted the docstring from numpy docstring to google style
docstring.

```python
def fire(planet: str):
    """Fire the deathstar laser at a planet

    Args:
        planet : Name of the planet to obliterate.
    """
    rich.print(f"💥 Firing laster at [red]{planet}[/red]")
```

[mkdocstrings]: https://mkdocstrings.github.io/

### Coverage Report

We run tests now in our project but what we don't do is look at the test
coverage.
Coverage means how much of the code is covered by tests.
Coverage is a tricky metric as there are different types such as branch
coverage, line coverage etc.
Note some teams set thresholds to trigger failing pipelines if the coverage is
too low.

Coverage is a neat thing but if you do things professionally it is a good 
practice to document the code coverage.
Thus we want to include this coverage report in our docs too.

First modify `pytest` in our `Taskfile.yaml` to make a coverage report and
output it as html:

```yaml
  test:
    desc: Runs tests on the code
    cmds:
      - >
        poetry run pytest
        --cov=deathstar
        --cov-report=html
```

This will create a folder `htmlcov` containing a very beautiful report.
Now to include this report we need another mkdocs plugin called
`mkdocs-coverage`.

```bash
poetry add --dev mkdocs-coverage
```

Next we modify our `mkdocs.yml` to use the plugin and use the generated report:

```yaml
# Some general page information
site_name: Deathstar 💥
site_url: https://Tea-n-Tech.github.io/deathstar/

# We want to use the material theme
theme:
  name: material

# The pages which you want to add
nav:
  - Home: index.md
  - Quick-Start: quick_start.md
  - FAQ: faq.md
  - Source Code: source_code.md
  - Coverage report: coverage.md

plugins:
  - search
  - mkdocstrings
  - coverage
```

When you run now `task docs-serve` you should see a page with a coverage report.
Really nice!
Lastly we should generate this coverage report everytime we build the docs.
Therefor we need to make the command `task test` a dependency of
`task docs-serve` in `Taskfile.yaml`.

```yaml
# ...
  test:
    desc: Runs tests on the code
    cmds:
      - >
        poetry run pytest
        --cov=deathstar
        --cov-report=html

  docs-serve:
    desc: Serve the documentation locally
    deps:
      - test
    cmds:
      - poetry run mkdocs serve
# ...
```

Now everytime we run `task docs-serve`, the command `task test` will
automatically run first.
So easy, we love you task ❤️

### SBOM

TODO
