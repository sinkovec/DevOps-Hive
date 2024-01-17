"""
Module to define in-memory database of some nearby located Sense Boxes.
"""
from .model import SenseBox, Sensor

SENSE_BOXES_DB = [
    SenseBox(
        "62221953b527de001b58de79",
        "Herzogenrath",
        [Sensor("62221953b527de001b58de7c", "Lufttemperatur")],
    ),
    SenseBox(
        "61ed83f8f4d1e2001c350c77",
        "Kerkrade-Centrum",
        [Sensor("61ed83f8f4d1e2001c350c7b", "Temperature")],
    ),
    SenseBox(
        "61e6c8ffac538c001b9f4bf0",
        "Herzogenrath Merkstein",
        [Sensor("61e6c8ffac538c001b9f4bf1", "Temperatur")],
    ),
]
