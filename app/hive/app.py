"""
Main entrypoint of the hive app.
"""
import importlib.metadata

from fastapi import FastAPI

app = FastAPI()

def version():
    """
    Returns the current version of the deployed app.
    """
    return importlib.metadata.version("hive")


@app.get("/version")
def read_version():
    """
    GET method to return the current app version.
    """
    return version()
