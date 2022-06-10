import os
import json

def test_umap():
    """
    Test the course similarity condition
    """
    rec = courserecommender()
    output = rec.get_umap(['ECE 143'])
    assert len(output.points)>0 and isinstance(output.points['ECE 143'],vector)

def test_recommendation():
    """
    Test the recommmender with key word and course name
    """
    rec = courserecommender()
    output = json.loads(rec.get_recommendation(input_string=['ECE 143','Signal'],number_of_recommend=10).json())
    assert len(output['recommend_set'])==2 
    # course with itself as the highest so removing first course so less course
    assert len(output['recommend_set']['ECE 143']['courses'])==9
    assert len(output['recommend_set']['Signal']['courses'])==10


