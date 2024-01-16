import importlib.metadata

def version():
    return importlib.metadata.version("hive")

def start():
    print(version())
