import typer
import uvicorn

from ..api import app

api_cmd = typer.Typer(name="api", invoke_without_command=True)


@api_cmd.callback()
def run_api(host: str = "0.0.0.0", port: int = 8080):
    """Starts the API server"""
    uvicorn.run(app=app, host=host, port=port)
