import typer
import uvicorn

from roslaunch_analyze_server.app import app

cli = typer.Typer()


@cli.command()
def run(port: int = 8000):
    uvicorn.run(app, host="localhost", port=port)
