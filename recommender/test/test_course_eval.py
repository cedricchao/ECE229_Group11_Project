import pytest
import os
from recommender.course_eval import course_eval 
import pandas as pd
import re
from collections import defaultdict


def test_getprofname(datafilename='./data/data.csv'):
    """
    test the get profname for the given department
    """
    cou = course_eval()
    df = pd.read_csv(datafilename)
    deparments = {re.match('^[A-Z]{1,5}',name)[0] for  name in df['course'].unique()}
    profname = defaultdict(set)
    for _, row in df[['instr','course']].iterrows():
        depart = re.sub('[0-9\s]','',row['course'])
        if row['instr'] not in profname[depart]:
            profname[depart].add(row['instr'])
    for prof in profname['ECE']:
        assert prof in cou.getprofname('ECE')

def test_getdeptname(datafilename='./data/data.csv'):
    """
    Test the list of departments

    Args:
        datafilename (str, optional): filename of the data. Defaults to './data/data.csv'.
    """
    cou = course_eval()
    df = pd.read_csv(datafilename)
    deparments = {re.match('^[A-Z]{1,5}',name)[0] for  name in df['course'].unique()}
    assert 'ECE' in deparments

def test_radar_plot():
    """
    test if the radar plot return the course details
    """
    output1 = ['Recommend_Course','Rcmnd_Instr','Time',
           'GPA_Expected', 'GPA_Actual']
    cou = course_eval()
    out = cou.get_radar_plotdetails('ECE 143')
    assert out[0]==output1