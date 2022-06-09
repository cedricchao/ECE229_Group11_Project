Recommender System
=============================

Recommender system runs on fastapi and it recommends similar courses given the key words or course name.
It is currently using nearest neighbour algo on the sentence embedding of the course description scraped from the UCSD catalog websites.

Data Preparation
----------------------------

Embedding extraction is used to extract the embedding and store them in the numpy file.

**Data folder** has the data extracted and stored using embedding extraction file.
Umap embedding is used to plot the course similarity on 2D is also generated and stored in numpy file
along with this mapping between the course name and embedding index.

For nearest neighbour algorithm, we use Faiss library from facebook which is tested on 1B search points and it's fast.

requirment.txt comprises all python libraries used in the project.


Docker
------------------------

The Docker file has the instruction to containerize the application.
Docker image is already in docker hub and can be pulled by
docker pull sumukhbadam/recommender:latest

**To run without Docker**

pip install -r requirments.txt

**To run the uvicorn server**

uvicorn recommender.asgi:app --host 0.0.0.0

Recommender folder
----------------------

**asgi.py**: This file holds the function for get and post function for fast api

**dataobj.py**: We use pydantic for data model in fast api and this file has all data model

**Embedding_extraction.py**: This is used to prepare data for extracting embedding and umap features etc.

.. autofunction:: Embedding_extraction.extract_embedding

.. autofunction:: Embedding_extraction.get_embedding

.. autofunction:: Embedding_extraction.get_model

.. autofunction:: Embedding_extraction.get_umap_feature

course_eval.py: This file has class for getting course details for undergraduate like GPA etc

.. autofunction:: course_eval.course_eval.getprofname

.. autofunction:: course_eval.course_eval.getdeptname

.. autofunction:: course_eval.course_eval.get_radar_plotdetails

**recommendation.py**: This file has class which helps in getting recommendation and umap details for course.

.. autoclass:: recommendation.courserecommender
	:members:

	.. automethod:: __init__

**undergrade_recommendation.py**: This file has class which help in recommending class for three courses and extra constraints.

.. autoclass:: undergrade_recommendation.Planner
	:members:

	.. automethod:: __init__



Test Folder
-------------------

This folder contains files for test cases.

test_course_eval.py: This has test cases for course eval file.

.. autofunction:: test_course_eval.test_getprofname

.. autofunction:: test_course_eval.test_getdeptname

.. autofunction:: test_course_eval.test_radar_plot

test_recommendation.py: This has test cases for recommendation file.

.. autofunction:: test_recommendation.test_umap

.. autofunction:: test_recommendation.test_recommendation


test_undergrad.py: This has test cases for undergraduate recommendation with constraints.

.. autofunction:: test_undergrad.test_course_list

.. autofunction:: test_undergrad.test_planner


To run test cases use pytest or pytest test/(name of the file)

