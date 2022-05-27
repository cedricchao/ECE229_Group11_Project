import os
from pydantic import BaseModel
from typing import List

class recommend(BaseModel):
    courses:dict

class obj(BaseModel):
    recommend_set:dict[str,recommend]

class input(BaseModel):
    inputs:List[str]