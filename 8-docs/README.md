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

[arc42]: https://arc42.org/overview

## How to document code?

Now we know what to document but not how.
In Python it usually comes down to three solutions.

- [Markdown]
- [Sphinx]
- [Mkdocs]

In the beginning start with pure markdown.
It is cheap, gets nicely displayed in repos and costs you nothing in effort.
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
This branch is the branch to use for uploading static pages belonging to your
repo.
The branch DOES NOT contain the source code.
It is a so called orphan branch, meaning it has no connection to the coding
branches as it is just for docs.
The site data contains a file `index.html` which will be rendered automatically
by GitHub, so cool 😎

### Source Map

TODO

### Coverage Report

TODO

### SBOM

TODO
