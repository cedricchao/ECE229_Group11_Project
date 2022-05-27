from typing import List
from recommendation import courserecommender
from dataobj import obj,input
import json
from fastapi import FastAPI
import logging
logging.basicConfig(filename='log.txt', level=logging.INFO)
app = FastAPI()

recommender = courserecommender()

@app.post("/",response_model=obj)
def get_course(string:input)->obj:
    logging.info(string)
    return recommender.get_recommendation(string.inputs,10)
