# This folder contains the code for the frontend of the project ece229 course<br>
We are using flask api to host the website.<br>
templates: This folder has the static webpage elements required for flask<br>
data: This folder house the data used by the webpage
couse_eval.py: This file has the class used to get details of the undergraduate course like gpa etc<br>
dataobj.py: We use pydantic for data modeling and the data models are defined here.<br>
filter.py: This file has functions used to filter the courses based on inputs.<br>
Letter.py: This file has mapping from the grade to points<br>

The frontend and backend is connected by rest api .<br>
Flask loads the static file and the dynamic content are loaded using the ajax method.<br>
For ploting the graph on the webpage we use plotly js and ajax to get the data from dataend server.<br>

This code is contanirzed and can we directly used using docker:<br>
docker run -it -p 5000:5000 sumukhbadam/frontend
## Below step run and provides the ip of the flask  you can connect using that on local machine <br>
docker build . -t tagname <br>
docker run -it -p 5000:5000 tagname <br>
