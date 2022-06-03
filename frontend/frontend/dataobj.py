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

class bar(BaseModel):
    x:List
    y:List
    name:str
    type:str = 'bar'

class bardata(BaseModel):
    x: List
    y: List
    text: List
    name:str
    textposition:str = 'auto'
    hoverinfo:str = 'none'
    opacity: float = 1.0
    type:str = 'bar'
    color:str= 'rgb(49,130,189)'

class FilterHtmlData(BaseModel):
    table: str
