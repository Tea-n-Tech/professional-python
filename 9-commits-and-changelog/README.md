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

## Commit Message Style

TODO

## Changelog Generation

TODO
