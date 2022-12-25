import typer

from .laser import laser_cmd
from .api import api_cmd

app = typer.Typer(no_args_is_help=True)
app.add_typer(laser_cmd, name="laser")
app.add_typer(api_cmd)
