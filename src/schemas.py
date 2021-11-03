""" Pydantic модели
"""
from typing import List

from pydantic import BaseModel


class DataCsv(BaseModel):
    id: List[str]
