# Pre-Commit Hooks

Git can run scripts before an action occurs.
Why would I want that?
Once you have waited for your action pipeline for a few minutes
just to fail and find out you forgot to format the code ...
well yes would be cool if that would have happened up earlier.

Pre-commit hooks run a script before you run `git commit -m "..."`.
This means you can run your linting before making the commit.
This is neat since no one will forget to run the quality rules
before commiting and thus pushing code to the repository.

## Installing the Hook

In your project directory root, you can find a hidden directory
`.git` in which all your git information is stored.
There is automatically a directory `.git/hooks` in which a bunch
of scripts are located.
Now open the script `pre-commit.sample`, edit delete all content
except the first line and enter the linting command from the
`Taskfile.yaml`.
The content of the script will look like as follows:

```sh
#!/bin/sh

# Run all linters before making a commit.
# For more info see Taskfile.yaml in the project root.
task lint
```

Don't forget to add a comment for the sake of your co-workers.
Congrats, you are done.
The next time you will commit code with `git commit -m "..."`
your linter will check your code automatically.

## Distributing Pre-Commit Hooks

Because your script lies within `.git/hooks`, you cannot commit it
which means it is not shared among developers.
This is a common issue and tools exist which can load the pre-commit
script from another directory.
We will go for `pre-commit` here, what a nice name.
Do the usual and install the dev dependency:

```sh
poetry add --dev pre-commit
```

Then you will need a file `.pre-commit-config.yaml` in your project
root.
Unfortunately, this tool does not integrate with `pyproject.toml`.
Now fill it with the following content:

```yaml
repos:
  - repo: local
    hooks:
      - id: python-linting
        name: python-linting
        entry: task lint
        language: system
        types: [python]
```

You can test if it works through the following command:

```sh
poetry run pre-commit run --all-files
```

To clean up, rename `.git/hooks/pre-commit` to
`.git/hooks/pre-commit.sample` again.
The hook is not installed yet.
Let's first add the hooks install command to our `Taskfile.yaml`
install command:

```yaml
# ...
  install:
    desc: Installs the dependencies.
    cmds:
      - poetry install
      - poetry run pre-commit install
# ...
```

If we run `task install`, not only will we get all python
dependencies but also the pre-commit hook will be installed.
Very nice.
Everytime you run `git commit ...` now our linter will run
and this is avalable to every developer with an automated
installation.

## More Material

There is a [guide on hooks][hooks-guide] in case you search
for more in-depth details.

[hooks-guide]: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks#_git_hooks
