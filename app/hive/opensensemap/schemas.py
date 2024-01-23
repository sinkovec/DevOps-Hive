"""
This module defines Pydantic models for temperature-related functionality.
"""

from enum import Enum
from pydantic import BaseModel, FiniteFloat


class TemperatureStatus(str, Enum):
    """
    Enumeration class for representing temperature statuses.
    """

    NONE = "No values present"
    TOO_COLD = "Too Cold"
    GOOD = "Good"
    TOO_HOT = "Too Hot"


class TemperatureBase(BaseModel):
    """
    Pydantic model for representing temperature-related data.
    """

    status: TemperatureStatus
    temperature: FiniteFloat
