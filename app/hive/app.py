"""
Main entrypoint of the hive app.
"""
from importlib import metadata
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .opensensemap.router import router as open_sense_map_router

app = FastAPI()
app.include_router(open_sense_map_router)

Instrumentator().instrument(app).expose(app)

def version():
    """
    Returns the current version of the deployed app.
    """
    return metadata.version("hive")


@app.get("/version")
def read_version():
    """
    GET method to return the current app version.
    """
    return version()
