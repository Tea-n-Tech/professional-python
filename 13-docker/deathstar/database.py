from abc import ABC
from typing import Dict, Union
from pydantic import BaseModel


class Planet(BaseModel):
    """Class with information about the planet"""

    name: str


class PlanetDatabase(ABC):
    """This class represents a generic planet database interface"""

    async def get_planet(self, name: str) -> Union[Planet, None]:
        """Get a planet from the database

        Args:
            name: Name of the planet to retrieve
        """
        raise NotImplementedError()

    async def remove_planet(self, name: str) -> bool:
        """Removes a planet from the database

        Args:
            name: Name of the planet to remove
        """
        raise NotImplementedError()


class FakePlanetDatabase(PlanetDatabase):
    planets: Dict[str, Planet]

    def __init__(self):
        # Create fake data
        self.planets = {
            "alderaan": Planet(name="Alderaan"),
            "tatooine": Planet(name="Tatooine"),
            "naboo": Planet(name="Naboo"),
            "tython": Planet(name="Tython"),
            "dantooine": Planet(name="Dantooine"),
            "yavin4": Planet(name="Yavin4"),
        }

    async def get_planet(self, name: str) -> Union[Planet, None]:
        return self.planets.get(name.lower())

    async def remove_planet(self, name: str) -> bool:
        name = name.lower()
        if name in self.planets:
            self.planets.pop(name)
            return True

        return False
