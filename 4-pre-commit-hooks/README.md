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

## More Material

There is a [guide on hooks][hooks-guide] in case you search
for more in-depth details.

[hooks-guide]: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks#_git_hooks
