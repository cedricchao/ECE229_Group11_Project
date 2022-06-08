Recommender system run on fastapi and it use to recommend the course given the key words or course name.<br>
It is currently using nearest neighbour algo on the sentence embedding of the course description scrapped from the ucsd website.<br>
<br>
Data Preparation:<br>
Embedding extraction is used to extract the embedding and store them in the numpy file.<br>
Umap embedding used to plot the course similarity on 2d is also generated and stored in numpy file.<br>
Along with this mapping between the  course name and embedding index<br>
<br>
For nearest algorithm we use Faiss library from facebook which is tested on 1B search points and its fast<br>

Recommender folder:<br>
    asgi.py: This file holds the function for get and post function for fast api<br>
    dataobj.py: We use pydantic for data model in fast api and this file has all data model<br>
    Embedding_extraction.py: This is used to prepare data for extracting embedding and umap features etc.<br>
    recommendation.py: This file has class which helps in getting recommendation and umap details for course.<br>
    undergrade_recommendation.py: This file has class which help in recommending class for three courses and extra constraints.<br>
    course_eval.py: This file has class for getting course details for undergraduate like gpa etc<br>
<br>
test Folder:<br>
    test_course_eval.py: This has test cases for course eval file.<br>
    test_recommendation.py: This has test cases for recommendation file.<br>
    test_undergrad.py: This has test cases for undergraduate recommendation with constraints.<br>
To run test cases use pytest or pytest test/(name of the file)<br>
<br>
Data:<br>
    This folder has the data extracted and stored using embedding extraction file.<br><br>
<br>
requirment.txt has all libraries used.<br>

The Docker file has the instruction to containerize the application.<br>
Docker image is already in docker hub and can be pulled by <br>
docker pull sumukhbadam/recommender:latest <br>
<br>
To run without Docker<br> 
do pip install -r requirments.txt<br>
to run the uvicorn server <br>
uvicorn recommender.asgi:app --host 0.0.0.0<br>