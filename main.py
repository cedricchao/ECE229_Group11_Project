from flask import Flask
from flask import render_template
from flask import request
import requests
import json
from couse_eval import course_eval
from dataobj import radar,radardata

course_eval_obj = course_eval()

app = Flask(__name__,static_folder='templates/public_html/assets',
            template_folder='templates/public_html')

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/getcourse', methods=['POST','GET'])
def getcourse():
    if request.method == 'POST':
        url = 'http://127.0.0.1:8000/recommend'
        myobj = {'inputs': request.json['body']}
        x = requests.post(url, data = json.dumps(myobj))
        print(x.json())
        return json.dumps(list(x.json()['recommend_set'][request.json['body'][0]]['courses'].keys()))
    return 'hello world'

@app.route('/getgraph', methods=['POST','GET'])
def getgraph():
    if request.method != 'POST':
            return
    url = 'http://127.0.0.1:8000/umap'
    myobj = {'inputs': request.json['body']}
    points = requests.post(url, data = json.dumps(myobj))
    points = points.json()['points']
    x = []
    y = []
    text = []
    for i,j in points.items():
        x.append(j['x'])
        y.append(j['y'])
        text.append(i)
    return json.dumps({'x':x,'y':y,'text':text})

@app.route('/getradar',methods=['POST','GET'])
def getradar():
    if request.method != 'POST':
        return
    string = request.json['body'][0]
    data = []
    for course in string.split(","):
        r,t = course_eval_obj.get_radar_plotdetails(course)
        if r is None:
            continue
        data.append(radar(r=r,theta=t,name=course))
    return radardata(data=data).json()



    