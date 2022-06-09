from .recommendation import courserecommender
from .undergrade_recommendation import Planner
from .dataobj import obj,input,vectordict,coursereq
import json
from typing import List,Dict
from fastapi import FastAPI
# import logging
# logging.basicConfig(filename='log.txt', level=logging.INFO)
app = FastAPI()

recommender = courserecommender()
planner = Planner()

@app.post("/recommend",response_model=obj)
def get_course(string:input)->obj:
    return recommender.get_recommendation(string.inputs,10)

@app.post("/umap",response_model=vectordict)
def get_points(string:input)->vectordict:
    return recommender.get_umap(string.inputs)

@app.post('/plan',response_model=List[Dict])
def get_planner(courses:List[coursereq])->List[Dict]:
    print(courses)
    return planner.get_recommendation(courses)
