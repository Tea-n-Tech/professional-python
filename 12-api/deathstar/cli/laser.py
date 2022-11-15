import typer

from ..laser import fire

laser_cmd = typer.Typer(no_args_is_help=True)


@laser_cmd.command(name="fire")
def fire_cmd(planet: str):
    fire(planet)
