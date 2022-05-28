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
    department = np.unique([c.split()[0] for c in df['course']])
    if dep not in department:
        raise Exception("Department does not exist")
    
    return df[[c.split()[0] == 'CSE' for c in df['course']]]
        


if __name__ == '__main__':

    df = pd.read_excel('data/data.xlsx')
    df = df.drop(['Unnamed: 0'], 1)

    #