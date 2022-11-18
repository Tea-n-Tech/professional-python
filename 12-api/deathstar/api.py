from fastapi import FastAPI, HTTPException, status

from .database import FakePlanetDatabase, Planet


app = FastAPI()
db = FakePlanetDatabase()


@app.delete("/api/v1/planets/{target}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_planet(target: str):
    """Shoot a laser at a planet

    Args:
        target: Planet name to destroy
    """
    success = await db.remove_planet(target)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planet {target} does not exist",
        )


@app.get("/api/v1/planets/{name}", response_model=Planet)
async def get_planet(name: str) -> Planet:
    """Get info about a planet

    Args:
        name: Name of the planet
    """
    planet = await db.get_planet(name)
    if planet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planet {name} does not exist",
        )

    return planet
