
# Professional Python

Learn to code professional Python.

## Requirements

- Python Basics
- Git Basics
- GitHub/GitLab/Bitbucket Basics
- Linux/Windows Commandline Basics (Linux recommended)

## Tasks

### Task 1 - Weather Data

Create a python program to fetch and print weather data:

- Start with a simple script
- Get weather data for the past and/or future 3 days
- Output the weather data to the console
- As weather data choose temperature and/or rainwater

Important

- Do a [pull request][github-pr] to make your submission in your repo
- Find someone to review your code (you can use our [discord])

[github-pr]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
[discord]: https://discord.gg/wEUHwtr8Pn

### Task 2 - GitHub CLI

Create a python program to interact with GitHub and retrieve data.
Add the following commands:

- Count all stars of all repos of yourself, a specified user or an organization.
- Print out details about yourself, a user or organization.
  Allow a nicely printed format as default and offer output as json too.
- One of the following:
  - (easy) Modify your user description by adding a tea emoji and a heart.
  - (difficult) Set your user status (top-right when clicking on username)
    to a tea emoji with the message "Drinking Tea".

Focus points:

- End-users will use your program so focus on usability
- Integrate previous lessons as much as it makes sense

### Task 3 - API

This task will be an advancement of the previous one by wrapping the
functionality in an API.
Create an API with the following routes:

- GET `/health/ping` to check if the API is up (can be unauthenticated)
- Require a GitHub token as authentication header and use this token for
  your API calls to GitHub within your API
- GET `/user` to get details about the currently authenticated user
- GET `/user/stars` to retrieve the amount of GitHub stars of all repos from the
  authenticated user
- GET `/user/{username}` to get data about the specified user
- GET `/user/{username}/stars` to get the amount of total stars from all repos
  of the specified user
- GET `/user/status` to get the current status of the authenticated user (see
  task 2)
- POST `/user/status` to set the users status to drinking tea (see task 2)

What is important?

- Document your API endpoints (hint: if you do this right, it is done
  automatically)
- The API needs to be wrapped and published as a docker image
- Add a task command to start the docker image (makes life easier)

## Lessons

- Lesson 1
  - [x] Package Management
- Lesson2
  - [x] Linting
  - [x] Formatting
  - [x] Typechecks
  - [x] Commands with Task
- Lesson 3
  - [x] Gitignore
- Lesson 4
  - [x] Licenses
- Lesson 5
  - [x] Continuous Integration (CI)
  - [x] GitHub Actions
- Lesson 6
  - [x] ~~Pre-commit hooks~~ (optional)
- Lesson 7
  - [x] Unit-Tests
- Lesson 8
  - [x] Docs generation
- Lesson 9
  - [x] Changelog and commit messages
- Lesson 10
  - [x] Command Line Interfaces (CLI)
- Lesson 11
  - [x] Releases git-flow
- Lesson 12
  - [x] API
- Lesson 13
  - [ ] Docker
