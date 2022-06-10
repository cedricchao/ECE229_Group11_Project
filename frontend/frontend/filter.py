import pandas as pd
import numpy as np

from .Letter import *



def letter_grade_filter(df, letter):
    '''
    letter: lower bounds for desired letter grade
    '''
    
    if letter not in set(grades):
        raise Exception("Invalid letter grade")
    
    df['letter_actual'] = [Letter(l) for l in df['letter_expected']]
    
    return df[df['letter_actual'] >= Letter(letter)]
        

def gpa_filter(df, gpa):
    
    if gpa < 0 or gpa > 4:
        raise Exception("GPA out of bound")
    
    return df[df['gpa_actual'] >= gpa]


def time_filter(df, time):
    if time < 0:
        raise Exception("Working hour out of bound")
    
    return df[df['time'] <= time]
    
        
def recommend_class_filter(df, ratio):
    if ratio < 0 or ratio > 1:
        raise Exception("Recommendation ratio out of bound")
        
    return df[df['rcmnd_class'] > ratio]


def recommend_instr_filter(df, ratio):
    if ratio < 0 or ratio > 1:
        raise Exception("Recommendation ratio out of bound")
        
    return df[df['rcmnd_instr'] > ratio]


def department_filter(df, dep):
    '''
    dep: list of string
    '''
    dep = set(dep)

    department = set(np.unique([c.split()[0] for c in df['course']]))
    if not dep.issubset(department):
        raise Exception("Department does not exist")
    
    return df[[c.split()[0] in dep for c in df['course']]]
        
class Filter():
    """
    Filter class is used to retrieve recommended courses based on input filters
    """
    def __init__(self, df_path):
        """
        Initialize Filter

        :param df_path: directory path of dataframe of all UCSD courses
        :type df_path: str
        """
        self.df = pd.read_csv(df_path)

    def run(self, letter=None, gpa=None, time=None, rec_class=None, rec_instr=None, dep=None):
        """
        Run the filter and provide recommended courses along with descriptions

        :param letter: letter grade e.g. A-, B+, A+
        :param gpa: 3.2, 3.8
        :type gpa: float
        :param time: weekly study hours e.g. 10, 20
        :type time: float
        :param rec_class: probability for class to be recommended in [0, 1]
        :type rec_class: float
        :param rec_instr: probability for instructor to be recommended in [0, 1]
        :type rec_instr: float
        :param dep: list of department codes e.g. CSE, ECE, PHIL
        :type dep: List[str]
        :return: dataframe of recommended courses
        """
        assert not dep or isinstance(dep, list)

        df = self.df.copy()
        if letter:
            df = letter_grade_filter(df, letter)
        
        if gpa:
            df = gpa_filter(df, float(gpa))

        if time:
            df = time_filter(df, float(time))

        if rec_class:
            df = recommend_class_filter(df, float(rec_class))

        if rec_instr:
            df = recommend_instr_filter(df, float(rec_instr))

        if dep:
            df = department_filter(df, dep)

        return df
