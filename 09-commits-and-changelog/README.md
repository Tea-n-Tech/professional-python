# Commits and Changelog

You have already been working a bit with commits now.
There are common practices for commits and commit naming but I also warn you
that they strongly vary across different open-source projects and companies.
For example a well-contained internal codebase does not need to follow very
strict guidelines since everyone of the team usually communices with each other
anyway.
In an open-source project, people will kiss you if you provide them with
beautifully concise commit messages to understand why you did what.

## Pull Request Merge Strategies

How you should name your commits depends strongly on your PR merge strategy.
On GitHub you can perform [three kinds of merges][gh-merge-strategies]:

1. Merge commit: Add all commits from the head branch to the base branch with a
   merge commit.
2. Squash merging: Combine all commits from the head branch into a single commit
   in the base branch.
3. Rebase merging: Add all commits from the head branch onto the base branch
   individually.

The *normal merge* will use a so called merge commit on the branch you emrge into
to connect the history.
Conflicts during the merge need to be resolves manually but that is usually
o trouble at all.

*Squash commits* take all commits you did in your feature branch, squash them
into a single commit and apply that to the base branch.
This is reallt nice since everyone usually writes unimportant commit messages
such as `save wip`, `add changes`, `test ci` and infinite more.
We would usually find them also in the general commit history, but especially
for bigger projects it is smart to simply use a single commit per PR and that
is it.

*Rebase merging* as the name states applies all changes to the base branch and
that's it. You will similarly to a normal merge retain everything that has
happened within the PR.

[gh-merge-strategies]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github

### Which Strategy to Choose?

Most people go with (1) but only since this is the default setting.
For a cleaner setup I recommend (2) as you throw away the dirty wip commits
and you can just go wild in your PR without feeling any guilt of polluting the
codebase.
There is another benefit of (2).
You only need to write a single, clean commit message during the merge.
These commit messages when adhering to a specific style can be parsed by certain
tools to automatically create a changelog between versions.
So useful 👀 Never write your changelogs manually.

## Commit Messages

How thoroughly you follow commit messages depends on the context.
As you noticed every commit must have a general message such as below:

```bash
git commit -m "this is the main message"
```

Commit messages can also be longer.
In such a case this main message is the first line and below you can enter
more details.
In most corporate environments more details are rarely required since the teams
know each other well enough.
In an open-source project it is imperative that everyone knows what you did
without being well-connected.
Longer messages become more crucial as people are more disconnected.
So writing a short list of the most important changes and why you did them
bridges this disconnection.

### Changelog Styles

The most important changelog styles are:

- [keep a changelog][keep-a-changelog]
- [angular style changelog][angular-style]

Smaller projects often follow the idiomatic and simpler
[keep a changelog][keep-a-changelog] and a lot of tools do too.

Here's the most important part from it:

Guiding Principles:

- Changelogs are for humans, not machines.
- There should be an entry for every single version.
- The same types of changes should be grouped.
- Versions and sections should be linkable.
- The latest version comes first.
- The release date of each version is displayed.
- Mention whether you follow Semantic Versioning.

Types of changes:

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

There is also another popular changelog format to follow which is the
[angular style changelog][angular-style].
It gives the option to distinguish between components better.
This comes from it's format `component: what was done`.

Components can be:

- `build`: Changes that affect the build system or external dependencies
  (example scopes: gulp, broccoli, npm)
- `ci`: Changes to our CI configuration files and scripts
  (example scopes: Circle, BrowserStack, SauceLabs)
- `docs`: Documentation only changes
- `feat`: A new feature
- `fix`: A bug fix
- `perf`: A code change that improves performance
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `style`: Changes that do not affect the meaning of the code (white-space,
  formatting, missing semi-colons, etc)
- `test`: Adding missing tests or correcting existing tests

which covers a majority of use-cases nicely.
As a professional choice **I advice going with angular style**.
For the sake of this small tutorial, we will stick with keep a changelog.
The tooling chosen in this tutorial can handle both formats.

[keep-a-changelog]: https://keepachangelog.com/en/1.0.0/
[angular-style]: https://gist.github.com/brianclements/841ea7bffdb01346392c

## Changelog Generation

As you guessed it, there are tools to generate a changelog for you if you follow
the changelog formats above.
We will do that now and include that changelog in our docs.
First we install `git-changelog` to do that.

```bash
poetry add --dev git-changelog
```

Now let's try it out:

```
> poetry run git-changelog .
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased

<small>[Compare with latest](https://github.com/Tea-n-Tech/professional-python/compare/aac118d3ffb54e4e837717a52d216fafdb8fe2ba...HEAD)</small>

### Added
- Add link ([00a1b2e](https://github.com/Tea-n-Tech/professional-python/commit/00a1b2e92d85caa763447a1ff8db645e194ad3f1) by codie).
...
```

Cool, there it is.
Seems I followed the right format to already generate a changelog.
Now let's get it into our docs.
Firstly we add a task to our `Taskfile.dev` to generate the changelog.

```yaml
# ...
  docs-serve:
    desc: Serve the documentation locally
    deps:
      - test
      - generate-changelog
    cmds:
      - poetry run mkdocs serve

  docs-publish:
    desc: Publish the documentation to gh-pages
    deps:
      - generate-changelog
    cmds:
      - poetry run mkdocs build
      - poetry run mkdocs gh-deploy --force

  generate-changelog:
    desc: Generates the changelog
    cmds:
      - poetry run git-changelog --output CHANGELOG.md .

#...
```

See how it was made a dependency of every other docs-related task to make sure
it is fresh and juicy 🥭
Now add a changelog site to the `mkdocs.yml` file.

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
  - Changelog: changelog.md

plugins:
  - search
  - mkdocstrings
  - coverage

markdown_extensions:
  - pymdownx.snippets
```

Be aware we did not only add the additional page but also added in the lower
part a markdown extension to include files in files.
More about that in a second.
As you probably recognize we create in the root dir a file `CHANGELOG.md` but
now we require a file `docs/changelog.md`.
We can bridge this gap by filling `docs/changelog.md` with the following
content:

```md

--8<-- "./CHANGELOG.md"

```

The extension `pymdownx.snippets` allows us to include the generated
`CHANGELOG.md` in this place.
Why not simply put the `CHANGELOG.md` in that place in the first place?
The answer is you could make that work too but the you have to update that file
every now and then.
To soldify this and prevent us from having to commit the `CHANGELOG.md`
all the time add it to your `.gitignore`.

```text
# ...

# no dynamically generated changelog
# it will be part of the docs on the gh-pages branch
CHANGELOG.md
```

Nice, you can now generate your changelog automatically 
