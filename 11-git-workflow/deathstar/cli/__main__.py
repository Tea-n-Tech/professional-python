import typer

from .laser import laser_cmd

app = typer.Typer(no_args_is_help=True)
app.add_typer(laser_cmd, name="laser")

if __name__ == "__main__":
    app()
