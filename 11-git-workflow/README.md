
# Git Workflow

This lesson is not about coding but about git and related topics.
Git stands in the middle of every modern software company and there are rules
which most professionals follow.
I advise to follow these rules unless you are certain why to break them.

## Branches

To put it brief, there are usually the following, most common branches:

- `main` (or `master`) for production-ready code
- `develop` for the current state of development
- `feature/...` for new features or often also any kind of change
- `bugfix/...` for correcting bugs in the code 🐛
- `release/...` for release branches (more about that later)
- `hotfix/...` for making hotfixes directly onto `main`

These are the most common branches encountered.
You will definitely encounter more specific names too such as `ci/...` for
continuous integration changes.
So be prepared with a certain amount of flexibility when joining a new company.

## Main

The `main` branch is where the latest running and production-ready state is
available.There are basically two ways how companies tend to make releases.
One is to create a `tag` on main, which is like a name for a `commit`.
Then the CI/CD pipeline will be triggered on a tag event and upload and deploy
the new version.
This is common and advised when releasing a library or binary to users.

If a company hosts a service such as twitter or do Software as a Service (SaaS),
they deploy the current state of `main`.
So whatever lands on main gets deployed!
There are often additional security measures, such as a staged rollout to limit
new features to a small amount of users and of course the possibility to
rollback any time.
In case a service is released everytime there is a merge on main, GitHub has
an environment feature to support this.

So remember these rules of thumb:

- Use `tags` for libraries and binaries
- Use just `main` for deploying services but emply security and reliability 
  measures

## Develop

Develop is where all new features and the work of all developers comes together.
A developer for every new task spawns a branch off develop, implements something
and then merges back into develop.
When the develop is ready for a release, it is in a specific workflow explained
later merged into main and that is it.
For services, develop often has its own deployment to see if things work but
this instance is never recheable by the users.
There are no fixed rules though so depending on the needs of the developers to
see real traffic, some companies duplicate prod events and pipe them into
develop to see if things work.
Be flexible in mind and creativity to solve problems but be careful to protect
your user experience as it is the core of a product.

## Feature Branches

Whatever work is being done, it is usually done on a `feature/...` branch.
If you don't know which type to give a branch, make it a feature branch.
Since feature branch names ought to be unique too, names such as
`feature/fix-button` are obviously not specific enough.
To avoid writing essay branch names, you can simply add the ticket or github
issue number and people can see themselves: `feature/issue-13-fix-button`.
On GitHub you can also connect Pull Request with issues etc so there are many
more ways to add context too.
After finishing your work, create a Pull Request and ask a reviewer to take a
look at it.
Unreviewed code is an extreme exception in professional life.
If no one is around for real (vacation times), review your code yourself.
You will be surprised how much you will find when looking at your own code in
a PR.

Note there are similar derivatives such as `bugfix/...` which kind of just a
more specific version of `feature/...` so I won't go into detail with them.
It is just a different name.

## Releases

How is a software release made in a professional environment?
To but it blunt, there is once again a rough, golden path but note that releases
can be very different for every product depending on the tech stack.

TODO
