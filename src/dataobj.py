import os
from pydantic import BaseModel
from typing import List

class recommend(BaseModel):
    courses:dict

class obj(BaseModel):
    recommend_set:dict #[str,recommend]

class input(BaseModel):
    inputs:List[str]

class vector(BaseModel):
    x:float
    y:float

class vectordict(BaseModel):
    points:dict #[str,vector]


class coursereq(BaseModel):
    Time:float
    GPA_Actual:float
    Rcmnd_Instr:float
    Recommend_Course:float
    department:List[str]
    keyword:str

