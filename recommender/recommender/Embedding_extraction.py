import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from collections import defaultdict
import pickle as pk
import os


def extract_embedding(dataframe:pd.DataFrame,modelname:str='paraphrase-MiniLM-L6-v2',datadump:str='data')->None:
    """_summary_
    Function extract the embedding of the course description from the pandas dataframe.
    Sentence transformer is used to get the embedding of the course 

    Args:
        dataframe (pd.DataFrame): pandas dataframe with course name and course description
        modelname (str, optional): Any model with capability of generating sentence 
        info listed in the sentence transfomer lib. 
        Defaults to 'paraphrase-MiniLM-L6-v2'.
    """
    model = SentenceTransformer(modelname)
    sentence_embedding = []
    # mapping of course name to embedding index
    course_map = defaultdict(list)
    # extract only the course number and department from the names
    course_n=dataframe['Course_Name'].str.extract('(\w{1,4}\s\w{1,3}\w{0,})')
    course_desp={}
    for num,(i,j) in enumerate(zip(course_n[0],dataframe['Course_Description'])):
        if isinstance(j,float):
            continue
        # extracting the sentence embedding
        sentence_embedding.append(model.encode(j,normalize_embeddings=True))
        # multiple course appear in different deparment
        course_map[i].append(num)
        course_desp[i]=j
    sentence_embedding_np = np.array(sentence_embedding)
    course_map_back = {}
    # tracking back from index to course
    for i,j in course_map.items():
        for k in j:
            course_map_back[k]=i
    if not os.path.isdir(datadump):
        os.makedirs(datadump)
    # dump sentence embedding and dict for mapping
    np.save(os.path.join(datadump,'sentence_embedding'),sentence_embedding_np)
    # dump course map
    with open(os.path.join(datadump,'coursemap.pk'),'wb') as ftp:
        pk.dump(course_map,ftp)
    # dump course map reverse
    with open(os.path.join(datadump,'coursemap_back.pk'),'wb') as ftp:
        pk.dump(course_map_back,ftp)
    with open(os.path.join(datadump,'coursemap_despk.pk'),'wb') as ftp:
        pk.dump(course_desp,ftp)

def get_embedding(input_string:str,model:SentenceTransformer)->np.array:
    """
    Generates embedding using the model 
    Args:
        input_string (str): input string which is used for extraction of embedding
        model (SentenceTransformer): model used for sentence embedding extraction
                                    model should have encode function

    Returns:
        np.array: embedding of the sentence 
    """
    return model.encode(input_string,normalize_embeddings=True)

def get_model(modelname:str='paraphrase-MiniLM-L6-v2')->SentenceTransformer:
    """
    create obj of the sentence transformer for embedding extraction

    Args:
        modelname (str, optional): model name. Defaults to 'paraphrase-MiniLM-L6-v2'.

    Returns:
        SentenceTransformer: model of instance sentence transformer
    """
    return SentenceTransformer(modelname)

def get_umap_feature(sentence_embedding_file:str='data/sentence_embedding.npy',dumpfilename:str='data/umap_embedding.npy')->None:
    """
    used to dump the umap embedding from the sentence embedding to plot the similarity

    Args:
        sentence_embedding_file (str, optional): File name for sentence embedding. Defaults to 'data/sentence_embedding.npy'.
        dumpfilename (str, optional): name of the file to dump the umap features. Defaults to 'data/umap_embedding.npy'.
    """
    sentence_embedding_np = np.load(sentence_embedding_file)
    import umap
    u = umap.UMAP()
    embedding = u.fit_transform(sentence_embedding_np)
    np.save('data/umap_embedding',embedding)

if __name__ == '__main__':
    dataframe = pd.read_csv('./data/dataframe_comb.csv')
    extract_embedding(dataframe=dataframe)
