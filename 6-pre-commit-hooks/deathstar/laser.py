import rich


def fire(planet: str):
    """Fire the deathstar laser at a planet
    Parameters
    ----------
    planet : str
        Name of the planet to obliterate.
    """
    rich.print(f"💥 Firing laster at [red]{planet}[/red]")
