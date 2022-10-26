import rich


def fire(planet: str):
    """Fire the deathstar laser at a planet

    Args:
        planet : Name of the planet to obliterate.
    """
    rich.print(f"💥 Firing laser at [red]{planet}[/red]")
