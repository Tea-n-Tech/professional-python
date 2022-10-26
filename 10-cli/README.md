
# Command Line Interfaces (CLIs)

A lot of tooling in software business is based on command line interfaces
and not neccesarily webpages.
The reason are not exactly obvious but the command line is simply the central
hub where programmers work all the time.
It is cheap to build and allows automatization if done right.
At first, CLIs don't seem as sexy as a material website but they are brutally
efficient and have their own charm if given time and space ... and care.

## CLIs in the world of Python

There is a long history of different libs and how to build clis from scratch.
In this lesson we will spare you this but recommend you a golden path.
These are libraries I commonly encountered in projects:

- [argparse]
- [click]
- [typer]

There are a lot more libraries but rest assured that these are widely used.
Arparse is the original, vanilla way to do argument parsing.
Go for it if you have to or don't want to install a big dependency just for
some minor argument parsing in a script.
There is nothing wrong with simplicity.
For a good user-experience go with click or typer.
Click is the maybe most often used library for argument parsing.
Nonetheless it has its edges, this is why typer was built on top of click.
In newer projects I usually encounter typer more often than click.

[argparse]: https://docs.python.org/3/library/argparse.html
[click]: https://click.palletsprojects.com/en/8.1.x/
[typer]: https://typer.tiangolo.com/

## Building a CLI

Let's offer our module function as a CLI.
First we install typer:

```bash
poetry add typer[all]
```

Here is a bit of advice.
Cli wrapper and core functions should be kept separate.
At best you should only call a single function in your cli wrapper
which does the job.
This simplifies testing greatly as you could abstract away the entire
underlying layer if you like to.
Now let us create a separate source folder where we can put our cli commands:

```bash
# module dir
mkdir deathstar/cli
touch deathstar/cli/__init__.py
# main entry point
touch deathstar/cli/__main__.py
# subcommand 'laser'
touch deathstar/cli/laser.py
```

The `__main__.py` will be run if someone calls the module itself through
`python -m poetry run deathstar.cli`.
It is a good practice to exclude a module main function like that.
First we implement `deathstar/cli/laser.py`:

```python
import typer

from ..laser import fire

laser_cmd = typer.Typer(no_args_is_help=True)


@laser_cmd.command(name="fire")
def fire_cmd(planet: str):
    fire(planet)
```

As you can see we wrapped our internal functions with a typer cmd.
Could we wrap the original directly?
Yes, you could though as I stated keeping things separate is more clean.
Nonetheless try out what suits you better regarding testing.
I very much like `no_args_is_help` as it is more user friendly to print a help
if no arguments to a command holding subcommands are specified.
Next is `touch deathstar/cli/__main__.py`

```python
import typer

from .laser import laser_cmd

app = typer.Typer(no_args_is_help=True)
app.add_typer(laser_cmd, name="laser")

if __name__ == "__main__":
    app()
```

That's it.
But how do we trigger it?
Try running as shown above:

```bash
> poetry run python -m deathstar.cli
                                                                              
 Usage: python -m deathstar.cli [OPTIONS] COMMAND [ARGS]...                     
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ laser                                                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Okay that is fancy.
Try running `poetry run python -m deathstar.cli laser fire`.
Another important hint here, be very very careful with grouping commands.
You don't want to have a group with just a single member.
Start a group if you are 555% sure that there will be more coming.

Another secret hint, be very careful around user-facing behaviour.
The command `deathstar laser fire` doesn't feel intuitive.
I would rather like something like `deathstar fire laser` which comes more
natural.
If `laser` truly is a resource shared by many commands then of course laser
coming first is the option to go but be aware to try out opposite ways and play
around for better feeling.

## Distributing the CLI

How do we distribute the CLI now?
What I want is that users can run the following command

```bash
deathstar fire laser "alderaan"
```

without all of that `poetry run -m ...` stuff in front.
We can register our cli main function as a script in our `pyproject.toml`:

```toml
# ...

[tool.poetry.scripts]
deathstar = "deathstar.cli.main:app"

# ...
```

If we now run `poetry build` to create our python wheel and ship it, users can
use our CLI as simple as follows:

```bash
python -m pip install deathstar
deathstar fire laser "alderaan"
```

Wow that is sweet that poetry takes care of this so easily and so well 🧁
A true blessing 👼

## User Experience

A few words of warning and advice here.
Customizing the user-experience is a delicate part.
Often we don't get it right the first time, that is natural.
Still, don't break stuff all the time and if you do so, increase the major
version respectively.
If you suffer from german anxienty and are catatonic when thinking about
changing the user-experience, go ahead and be more bold.
Breaking stuff is natural.
Just always think about what it means for the users.
If breaking things is a big gain and if you break stuff how could you make the
transition easier?
For example an error or help message might do the job already to easy any
trouble on the horizon.
The golden rule here is, there is no golden rule for a very good user
experience, but the secret ingredient is love and empathy for your users ❤️ and
the joy when using the tool 🪄✨
