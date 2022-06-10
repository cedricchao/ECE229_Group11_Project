import pytest
import os
from recommender.undergrade_recommendation import Planner
from recommender.dataobj import coursereq

def test_course_list():
    """
    test if the recommendation for a key is from the input department only
    """
    plan = Planner()
    out = plan.get_course_list(['ECE'],'signal')
    for cou in out:
        assert 'ECE' in cou.split()[0]

def test_planner():
    """
    Test the planner
    """
    courses=[
    coursereq(GPA_Actual=4,Time=(10/10)*4,Rcmnd_Instr=4,Recommend_Course=3.6,department=['ECE','CSE'],keyword='Digital signal Processing'),
    coursereq(GPA_Actual=3,Time=(5/10)*4,Rcmnd_Instr=4,Recommend_Course=3.6,department=['ECE','CSE','MATH'],keyword='Machine Learning'),
    coursereq(GPA_Actual=3.5,Time=(10/10)*4,Rcmnd_Instr=4,Recommend_Course=3.6,department=['ECE','CSE','MATH'],keyword='Optimization')]
    planner = Planner()
    output = planner.get_recommendation(courses)
    assert len(output)>=0 
    if len(output)>0:
        assert isinstance(output[0],dict)

    

    



