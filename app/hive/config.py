"""
Dynaconf settings module.
"""
import os
from dynaconf import Dynaconf

current_directroy = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(root_path=current_directroy, settings_files=["settings.toml"])
