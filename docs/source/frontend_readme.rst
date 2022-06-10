Frontend
=================

We are using flask api to host the website.
The frontend and backend are connected by rest api.

Flask and docker 
---------------------

Flask loads the static file and the dynamic content are loaded using the ajax method.
For ploting the graph on the webpage, we use plotly js and ajax to get the data from dataend server.

This code is containerized and it can be directly accessed using docker:

docker run -it -p 5000:5000 sumukhbadam/frontend

Below step run provides the IP of the flask you can connect to on your local machine:

docker build . -t tagname
docker run -it -p 5000:5000 tagname

Frontend components
--------------------------------

**templates**: This folder has the static webpage elements required for flask

**data**: This folder houses the data used by the webpage 

.. autoclass:: couse_eval.course_eval
	:members:

	.. automethod:: __init__

**dataobj.py**: We use pydantic for data modeling and the data models are defined here.

**filter.py**: This file has functions used to filter the courses based on inputs.

.. autoclass:: filter.Filter
	:members:

	.. automethod:: __init__

**Letter.py**: This file has mapping from the grade to points

.. autoclass:: Letter.Letter
	:members:

	.. automethod:: __init__

Test Folder
----------------------

**test**: This folder has the test case for python files

.. autofunction:: test_course_eval.test_getprofname

.. autofunction:: test_course_eval.test_getdeptname

.. autofunction:: test_course_eval.test_radar_plot



