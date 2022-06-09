from ast import keyword
from course_eval import course_eval
import numpy as np
import pickle as pk
from sentence_transformers import SentenceTransformer
import faiss
import scipy
import pandas as pd
from dataobj import coursereq, recommend
from typing import List,Dict

class Planner():
    """
    Helps to plan the course
    """
    def __init__(self,
                course_map_file:str='data/coursemap.pk',
                coursemap_back_file:str='data/coursemap_back.pk',
                coursemap_desp_file:str='data/coursemap_despk.pk',
                embedding_file:str='./data/sentence_embedding.npy') -> None:
        """
        Help to plan the course for the quater given the three course key and additional inputs 
    
        :param course_map_file: _description_. Defaults to 'data/coursemap.pk'.
        :type course_map_file: str
        :param coursemap_back_file: _description_. Defaults to 'data/coursemap_back.pk'.
        :type coursemap_back_file: str
        :param coursemap_desp_file: _description_. Defaults to 'data/coursemap_despk.pk'.
        :type coursemap_desp_file: str
        :param embedding_file: _description_. Defaults to './data/sentence_embedding.npy'.
        :type embedding_file: str
        """
        with open(course_map_file,'rb') as ftp:
            self.course_map = pk.load(ftp)
        with open(coursemap_back_file,'rb') as ftp:
            self.course_map_back = pk.load(ftp)
        with open(coursemap_desp_file,'rb') as ftp:
            self.coursemap_desp = pk.load(ftp)
        self.sentence_embedding_np = np.load(embedding_file)
        
        self.df = pd.read_csv('data/data.csv')
        self.modelname='paraphrase-MiniLM-L6-v2'
        self.model = SentenceTransformer(self.modelname) 
        self.course_data = course_eval()
        self.info_key = set(self.df['course'])
        self.course_data = course_eval()

    def get_course_list(self,department:List[str],course_key:str,num_of_course:int=10) -> List:
        """
        Return similar courses from selected department and 
        returned list of courses has len same as num of course
        
        :param department: List of department names used to recommend the course from 
        :type department:  List[str]
        :param course_key: key of the course which the resultant course should be similar to 
        :type course_key:  str
        :param num_of_course: length of courses that is similar to the key. Defaults to 10.
        :type num_of_course: int
        :return: List: returns the list of courses that match the course key
        """
        course_mini_map={}
        for i in self.info_key:
            if i  in self.course_map and (i.split()[0] in department):
                course_mini_map[i]=self.course_map[i][0]
        sentence_embedding_np_small = self.sentence_embedding_np[list(course_mini_map.values())]
        course_mini_map_back = {i:name for i,name in enumerate(course_mini_map.keys())}
        course_mini_map = {name:i for i,name in enumerate(course_mini_map_back.values())}
        fai = faiss.IndexFlatL2(384)
        fai.add(sentence_embedding_np_small)
        D,I = fai.search(self.model.encode(course_key,normalize_embeddings=True).reshape(1,-1),num_of_course)
        return [course_mini_map_back[i] for i in I[0]]
    
    def get_recommendation(self,courses:List[coursereq]) -> List[Dict[str,coursereq]]:
        """
        Provide the list of possible combination of courses given requirements
        
        :param courses: List of Courses with requiements for each courses
        :type courses: List[coursereq]
        :return: Return the list of dict of possible combination of courses given requirements
        """
        list_a = self.get_course_list(courses[0].department,courses[0].keyword,5)
        list_b = self.get_course_list(courses[1].department,courses[1].keyword,5)
        list_c = self.get_course_list(courses[2].department,courses[2].keyword,5)
        final_list = dict(enumerate(set(list_a+list_b+list_c)))

        time_cost = np.zeros((3,len(final_list)))
        gpa_cost = np.zeros((3,len(final_list)))
        inst_cost = np.zeros((3,len(final_list)))
        cousr_cost = np.zeros((3,len(final_list)))

        for num,course in final_list.items():
            c_dict = dict(zip(*self.course_data.get_radar_plotdetails(course)))
            for j in range(3):
                time_cost[j,num] = c_dict['Time']-(courses[j].Time/10)*4
                gpa_cost[j,num] = courses[j].GPA_Actual - c_dict['GPA_Actual']
                inst_cost[j,num] = courses[j].Rcmnd_Instr*4 - c_dict['Rcmnd_Instr']
                cousr_cost[j,num] = courses[j].Recommend_Course*4 - c_dict['Recommend_Course']
        cost_weights=[[1,10,1,1],[10,1,1,1],[1,1,10,1],[1,1,1,10],[10,5,1,1],[5,10,1,1]]
        out = set()
        for cost_weight  in cost_weights:
            cost = sum(i*j for i,j in zip(cost_weight,[time_cost,gpa_cost,inst_cost,cousr_cost]))
            form,idx = scipy.optimize.linear_sum_assignment(cost)
            idx.sort()
            out.add(tuple(idx))
        output=[]
        for idx in out:
            cgpa=0
            remommend = {}
            for i in idx:
                c_dict = dict(zip(*self.course_data.get_radar_plotdetails(final_list[i])))
                cgpa+=c_dict['GPA_Actual']
                remommend[final_list[i]] = coursereq(Time=c_dict['Time']*2.5,
                                                    GPA_Actual=c_dict['GPA_Actual'],
                                                    Rcmnd_Instr=c_dict['Rcmnd_Instr']/4,
                                                    Recommend_Course=c_dict['Recommend_Course']/4,
                                                    keyword=self.coursemap_desp[final_list[i]],department=[])
            remommend['cgpa']=cgpa/3
            output.append(remommend)
        return output
        
# if __name__ == '__main__':
#     courses=[
#     coursereq(GPA_Actual=4,Time=(10/10)*4,Rcmnd_Instr=4,Recommend_Course=3.6,department=['ECE','CSE'],keyword='Digital signal Processing'),
#     coursereq(GPA_Actual=3,Time=(5/10)*4,Rcmnd_Instr=4,Recommend_Course=3.6,department=['ECE','CSE','MATH'],keyword='Machine Learning'),
#     coursereq(GPA_Actual=3.5,Time=(10/10)*4,Rcmnd_Instr=4,Recommend_Course=3.6,department=['ECE','CSE','MATH'],keyword='Optimization')]
#     planner = Planner()
#     print(planner.get_recommendation(courses))