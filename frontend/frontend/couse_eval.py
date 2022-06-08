from typing import List
import numpy as np
import pandas as pd
from typing import List
import os
from frontend.dataobj import bar,bardata
import re
from collections import defaultdict

class course_eval():
    """
    Course eval is used for to retrive the course eval data
    """
    def __init__(self,datafilename:str='data/data.csv') -> None:
        """
        Initialze the obj with the dataframe class
        Args:
            datafilename (str, optional): path for the data. Defaults to 'data/data.csv'.
        """
        assert os.path.isfile(datafilename),'file not present in the path'
        self.df = pd.read_csv(datafilename)
        self.deparments = {re.match('^[A-Z]{1,5}',name)[0] for  name in self.df['course'].unique()}
        self.profname = defaultdict(set)
        for _, row in self.df[['instr','course']].iterrows():
            depart = re.sub('[0-9\s]','',row['course'])
            if row['instr'] not in self.profname[depart]:
                self.profname[depart].add(row['instr'])
            
    def getprofname(self,department:str)->List:
        """
        Return the list of  prof names from the department
        Args:
            department (str): Name of the department

        Returns:
            List: prof names
        """
        return sorted(list(self.profname[department]))
    
    def getdeptname(self)->List:
        """
        Returns all the departments 
        Returns:
            List:  list of department name
        """
        return sorted(list(self.deparments))
    def get_radar_plotdetails(self,course:str)->List:
        """
        Return the Radar plot details for the given course
        Args:
            course (str): course name for to be plotted
        Returns:
            List: _description_
        """
        theta=['Recommend Course','Rcmnd Instr','Time',
           'GPA Expected', 'GPA Actual']
        if course not in set(self.df['course']):
            return None,None
        selected_course = self.df[self.df['course']==course]
        total_eval = sum(selected_course['evals'])
        recommend_course = sum(selected_course['evals']*selected_course['rcmnd_class'])/total_eval*4
        rcmnd_instr = sum(selected_course['evals']*selected_course['rcmnd_instr'])/total_eval*4
        time = sum(selected_course['evals']*selected_course['time'])/total_eval/10*4
        gpa_expected = sum(selected_course['evals']*selected_course['gpa_expected'])/total_eval
        gpa_actual = sum(selected_course['evals']*selected_course['gpa_actual'])/total_eval
        return (theta,[recommend_course,rcmnd_instr,time,gpa_expected,gpa_actual])

    def get_GPA_details(self,course:str)->List:
        """
        Return Bar plot details for the given course
        Args:
            course (str): course name for to be plotted
        

        Returns:
            List: _description_
        """
        if course not in set(self.df['course']):
            return None,None
        selected_course = self.df[self.df['course']==course] 
        y=selected_course.groupby('term')[['gpa_actual','gpa_expected']].agg('mean')
        trace1=bar(x=list(y.index),y=list(y['gpa_actual']),name= 'Actual GPA')
        trace2=bar(x=list(y.index),y=list(y['gpa_expected']),name= 'Expected GPA')
        return [trace1,trace2]

    def get_instr_details(self,instr:str)->List:
        """
        Return Bar plot details for the given course
        Args:
            course (str): course name for to be plotted
        

        Returns:
            List: _description_
        """
        if instr not in set(self.df['instr']):
            return None,None
        theta=['Rcmnd Instr','Time',
           'GPA Expected', 'GPA Actual']
        selected_instr = self.df[self.df['instr']==instr] 
        total_eval = sum(selected_instr['evals'])
        rcmnd_instr = (sum(selected_instr['evals']*selected_instr['rcmnd_instr'])/total_eval)*4
        time = (sum(selected_instr['evals']*selected_instr['time'])/total_eval/10)*4
        gpa_expected = sum(selected_instr['evals']*selected_instr['gpa_expected'])/total_eval
        gpa_actual = sum(selected_instr['evals']*selected_instr['gpa_actual'])/total_eval
        return ([rcmnd_instr,time,gpa_expected,gpa_actual],theta)
    
    def get_instr_course_info(self,instr:str)->List:
        grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
        grades = reversed(grades)
        grades = {l:i for i,l in enumerate(grades)}
        if instr not in set(self.df['instr']):
            return None,None
        selected_instr = self.df[self.df['instr']==instr] 
        letter_actual=selected_instr.groupby(['course','letter_actual'])['evals'].agg('sum').reset_index(name='count')
        letter_expected=selected_instr.groupby(['course','letter_expected'])['evals'].agg('sum').reset_index(name='count')
        letter_actual_Dict={};letter_expected_Dict={}
        for c in letter_actual['course'].unique():
            tempdf=letter_actual[letter_actual['course']==c]
            tempdf_exp=letter_expected[letter_expected['course']==c]
            tempdf=tempdf.groupby('letter_actual')['count'].agg(pd.Series.mode).reset_index(name='count')
            tempdf_exp=tempdf_exp.groupby('letter_expected')['count'].agg(pd.Series.mode).reset_index(name='count')
            myDict=tempdf.set_index('letter_actual').T.to_dict('list')
            myDict={i:v[0] for i,v in myDict.items()}
            myDict_exp=tempdf_exp.set_index('letter_expected').T.to_dict('list')
            myDict_exp={i:v[0] for i,v in myDict_exp.items()}
            letter_actual_Dict[c]=max(myDict, key=myDict.get)
            letter_expected_Dict[c]=max(myDict_exp, key=myDict_exp.get)
        trace1=bardata(x=list(letter_actual_Dict.keys()),y=[grades[v.strip()] for i,v in letter_actual_Dict.items()],text=list(letter_actual_Dict.values()), name= 'Actual letter grade')
        trace2=bardata(x=list(letter_expected_Dict.keys()),y=[grades[v.strip()] for i,v in letter_expected_Dict.items()],text=list(letter_expected_Dict.values()),name= 'Expected letter grade')
        return [trace1,trace2]


    