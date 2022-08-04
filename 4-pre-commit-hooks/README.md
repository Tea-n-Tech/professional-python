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

## More Material

There is a [guide on hooks][hooks-guide] in case you search
for more in-depth details.



[hooks-guide]: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks#_git_hooks
