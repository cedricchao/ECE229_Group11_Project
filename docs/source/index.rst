.. UCSD Course Recommender documentation master file, created by
   sphinx-quickstart on Sun Jun  5 18:24:10 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to UCSD Course Recommender's documentation!
===================================================

This is a project for ECE229 course work of Group 11.
We have built a recommendation system which helps UCSD students select courses for their quarter.
Whole project is split into two mini folders, namely, recommender and frontend.
Each mini system is isolated and communicate using http.
Recommender folder houses the code and test case for the recommendation system.
Frontend folder houses the code and test case for the website to host service.
Both the services are contanierized and can be easily run by the docker-compose.

Instruction to run docker-compose:
-----------------------------------------

Run docker-compose up -t test

This will run two docker containers.

Website IP and port=5000 can be used to open the link from the browser
ex: 172.10.0.2:5000/ -> will open the website


Contents
--------

.. toctree::

   frontend_readme
   recommender_readme

.. note::
    This project is under active development