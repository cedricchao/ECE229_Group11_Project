import pytest
import os
import pandas as pd
import numpy as np

from frontend.filter import *
from frontend.Letter import *

df = pd.read_csv('./data/data.csv')

def test_letter_filter():
    '''
    test expected behavior of letter grade filter
    '''
    a_minus = letter_grade_filter(df, 'A-')
    b_plus = letter_grade_filter(df, 'B+')
    b_minus = letter_grade_filter(df, 'B-')

    for _,row in a_minus.iterrows():
        assert row['letter_actual'] >= Letter('A-')

    assert len(a_minus) <= len(b_plus)
    assert len(b_plus) <= len(b_minus)

def test_gpa_filter():
    '''
    test expected behavior of gpa filter
    '''

    a_minus = gpa_filter(df, 3.6)
    b_plus = gpa_filter(df, 3.3)
    b_minus = gpa_filter(df, 3.0)

    for _,row in a_minus.iterrows():
        assert row['gpa_actual'] >= 3.6

    assert len(a_minus) <= len(b_plus)
    assert len(b_plus) <= len(b_minus)


def test_time_filter():
    '''
    test expected behavior of time filter
    '''

    short = time_filter(df, 2)
    long = time_filter(df, 5)

    for _,row in short.iterrows():
        assert row['time'] <= 2

    assert len(short) <= len(long)


def test_rec_class():
    '''
    test expected behavior of recommend class filter
    '''

    low = recommend_class_filter(df, 0.2)
    high = recommend_class_filter(df, 0.95)

    for _,row in high.iterrows():
        assert row['rcmnd_class'] >= 0.95

    assert len(high) <= len(low)


def test_rec_instr():
    '''
    test expected behavior of recommend instructor filter
    '''

    low = recommend_instr_filter(df, 0.2)
    high = recommend_instr_filter(df, 0.95)

    for _,row in high.iterrows():
        assert row['rcmnd_instr'] >= 0.95

    assert len(high) <= len(low)


def test_department_filter():
    '''
    test expected behavior of department filter
    '''

    cse = department_filter(df, ['ECE', 'CSE'])
    #ece = department_filter(df, ['ECE'])
    both = department_filter(df, ['ECE', 'CSE'])

    assert len(cse) <= len(both)