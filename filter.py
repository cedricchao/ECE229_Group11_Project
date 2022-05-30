import pandas as pd
import numpy as np

from Letter import *



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
    def __init__(self, letter=None, gpa=None, time=None, rec_class=None, rec_instr=None, dep=None):
        '''
        letter: string
        gpa: float
        time: float
        rec_class: float [0, 1]
        rec_instr: float [0, 1]
        dep: list of string
        '''
        assert isinstance(dep, list)

        self.letter = letter 
        self.gpa = gpa 
        self.time = time 
        self.rec_class = rec_class 
        self.rec_instr = rec_instr 
        self.dep = set(dep)

    def run(self, df):
        if self.letter:
            df = letter_grade_filter(df, self.letter)
        
        if self.gpa:
            df = gpa_filter(df, self.gpa)

        if self.time:
            df = time_filter(df, self.time)

        if self.rec_class:
            df = recommend_class_filter(df, self.rec_class)

        if self.rec_instr:
            df = recommend_instr_filter(df, self.rec_instr)

        if self.dep:
            df = department_filter(df, self.dep)

        return df


if __name__ == '__main__':

    # an example of using filter
    df = pd.read_excel('../data/data.xlsx')
    df = df.drop(['Unnamed: 0'], 1)

    # would like to filter out any CSE or ECE courses
    # that has less than 5 hours / week working hours
    # has a better letter grade than B+
    f = Filter(dep=['CSE', 'ECE'], time=5, letter='B+')
    print(f.run(df))