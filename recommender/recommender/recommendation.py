import numpy as np
import os
import pickle as pk
import faiss
from Embedding_extraction import get_embedding,get_model
from dataobj import recommend,obj,vectordict,vector

class courserecommender():
    """
    This is recommendation class which gives recommendation 
    given the course id or string 
    """
    def __init__(self,embedding_file:str='./data/sentence_embedding.npy',
                embedding_size:int=384,
                course_map_file:str='./data/coursemap.pk',
                coursemap_back_file:str='./data/coursemap_back.pk',
                coursemap_desp_file:str='./data/coursemap_despk.pk',
                umap_embedding_file:str='./data/umap_embedding.npy') -> None:
        """
        Reads the sentence embedding and loads the data for recommendation.
        
        :param embedding_file: file name with sentence embedding. Defaults to './data/sentence_embedding.npy'.
        :type embedding_file: str
        :param embedding_size: sentence embedding vector dimension. Defaults to 384.
        :type embedding_size: int
        :param course_map_file: pickle file with course map. Defaults to '.data/coursemap.pk'.
        :type course_map_file: str
        :param coursemap_back_file: pickle file with reverse course map . Defaults to './data/coursemap_back.pk'.
        :type coursemap_back_file: str
        :param coursemap_desp_file: pickle file with course description .Defaults to  './data/coursemap_despk.pk'.
        :type coursemap_desp_file: str
        :param umap_embedding_file: Umap embedding with for course .Defaults to  './data/umap_embedding.npy'.
        :type umap_embedding_file: str
        """
        assert os.path.isfile(embedding_file) and os.path.isfile(course_map_file) and os.path.isfile(coursemap_back_file),'File are not present as mentioned'
        assert embedding_size>0,'embedding dimension vector should be greater than 0' 
        self.index = faiss.IndexFlatL2(embedding_size)
        self.sentence_embedding_np = np.load(embedding_file)
        self.umap_embedding = np.load(umap_embedding_file)
        self.index.add(self.sentence_embedding_np)
        print(self.sentence_embedding_np.shape)
        with open(course_map_file,'rb') as ftp:
            self.course_map = pk.load(ftp)
        with open(coursemap_back_file,'rb') as ftp:
            self.course_map_back = pk.load(ftp)
        with open(coursemap_desp_file,'rb') as ftp:
            self.coursemap_desp = pk.load(ftp)
        self.model = get_model()
        self.sentence_embedding_extractor = get_embedding

    def get_recommendation(self,input_string:list,number_of_recommend:int)->obj:
        """
        Given the list of the string it provides the dict of recommended courses and description
        
        :param input_string: list of string they can be course number or string of topics
        :type input_string: List
        :param number_of_recommend: number of similar recommmended courses per string
        :type number_of_recommend: int
        :return: dict of string and for each string its a dict with course and its description
        """
        output={}
        for string  in input_string:
            if string in self.course_map:
                course_id = self.course_map[string]
                D,I = self.index.search(self.sentence_embedding_np[course_id],number_of_recommend)
                rec = recommend(courses={self.course_map_back[i]:self.coursemap_desp[self.course_map_back[i]]  for i in I[0][1:]})  
            else:
                string_np = self.model.encode(string)
                D,I = self.index.search(string_np.reshape(1,-1),number_of_recommend)
                rec = recommend(courses={self.course_map_back[i]:self.coursemap_desp[self.course_map_back[i]] for i in I[0]})
            output[string]=rec
        return obj(recommend_set=output)

    def get_umap(self,input_string:list)->vectordict:
        """
        Return the 2D vector position of the embedding of the course for visulization
        
        :param input_string: list of course name
        :type input_string: List
        :return: dict of the course and unit vector values for course
        """
        output={}
        print(input_string)
        for string  in input_string[0].split(","):
            if string in self.course_map:
                course_id = self.course_map[string]
                vec= vector(x=self.umap_embedding[course_id,0],y=self.umap_embedding[course_id,1])
                output[string]=vec
        return vectordict(points=output)
    


if __name__ == '__main__':
    import time
    recommender = courserecommender()
    r = time.time()
    print(recommender.get_recommendation(['ECE 273','Linear Algebra'],10))
    


        
        
