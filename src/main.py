from recommendation import courserecommender
from dataobj import obj,input,vectordict
import json
from fastapi import FastAPI
import logging
logging.basicConfig(filename='log.txt', level=logging.INFO)
app = FastAPI()

recommender = courserecommender()

@app.post("/recommend",response_model=obj)
def get_course(string:input)->obj:
    return recommender.get_recommendation(string.inputs,10)

@app.post("/umap",response_model=vectordict)
def get_points(string:input)->vectordict:
    return recommender.get_umap(string.inputs)