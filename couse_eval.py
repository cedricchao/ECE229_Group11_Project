from typing import List
import numpy as np
import pandas as pd
from typing import List
import os

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
        return ([recommend_course,rcmnd_instr,time,gpa_expected,gpa_actual],theta)