from pydantic import BaseModel
from typing import List,Dict

class radar(BaseModel):
    type:str = 'scatterpolar'
    r:List
    theta:List
    fill:str= 'toself'
    name:str

class radardata(BaseModel):
    data:List