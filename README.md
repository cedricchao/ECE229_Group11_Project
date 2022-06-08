# ECE229_Group11_Project<br>
This is a project for ECE229 course work of Group 11<br>
We have built a recommendation system which helps student in recommending course for their quarter.<br>
Whole project is split into two mini folder recommendation system and frontend<br>
Each mini system is isolated and communicate using http<br>
Recommender folder house the code and test case for the recommendation system.<br>
Frontend folder house the code and test case for the website to host service.<br>
Both the services are contanierized and can be easily run by the docker-compose<br>
Instruction to run docker-compose:<br>
docker-compose file is part of frontend folder.<br>

Run docker-compose up -t test <br>
this will run two docker containers<br>
Website IP and port=5000 can be used to open the link from the browser<br>
ex: 172.10.0.2:5000/ -> will open the website<br>

