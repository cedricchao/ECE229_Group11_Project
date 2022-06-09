from typing import List
import numpy as np
import pandas as pd
from typing import List
import os
import re
from collections import defaultdict

class course_eval():
    """
    Course eval is used for to retrive the course eval data
    """
    def __init__(self,datafilename:str='./data/data.csv') -> None:
        """
        Initialze the obj with the dataframe class
        
        :param datafilename: path for the data. Defaults to 'data/data.csv'.
        :type datafilename: str
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
        
        :param department: Name of the department
        :type department: str
        :return: prof names
        """
        return sorted(list(self.profname[department]))
    
    def getdeptname(self)->List:
        """
        Returns all the departments 
        
        :return: list of department name
        """
        return sorted(list(self.deparments))
        
    def get_radar_plotdetails(self,course:str)->List:
        """
        Return the Radar plot details for the given course
        
        :param course: course name for which radar plot is shown
        :return: _description_
        """
        theta=['Recommend_Course','Rcmnd_Instr','Time',
           'GPA_Expected', 'GPA_Actual']
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