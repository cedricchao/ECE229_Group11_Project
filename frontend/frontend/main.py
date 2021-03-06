from crypt import methods
from flask import Flask
from flask import render_template
from flask import request
import requests
import json
from .couse_eval import course_eval
from .dataobj import radar,radardata,bar,bardata,FilterHtmlData
from .filter import *
import os

df_path = './data/data.csv'
servicename='127.0.0.1'
if "Servicename" in os.environ:
    servicename= os.getenv('Servicename')

course_eval_obj = course_eval()
filter_obj = Filter(df_path = df_path)



app = Flask(__name__,static_folder='templates/public_html/assets',
            template_folder='templates/public_html')

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/getcourse', methods=['POST','GET'])
def getcourse():
    if request.method == 'POST':
        url = 'http://{0}:8000/recommend'.format(servicename)
        myobj = {'inputs': request.json['body']}
        x = requests.post(url, data = json.dumps(myobj))
        dic={}
        dic['data']=[list(x.json()['recommend_set'][request.json['body'][0]]['courses'].keys()),
                    list(x.json()['recommend_set'][request.json['body'][0]]['courses'].values())]
        return json.dumps(dic)
    return 'hello world'

@app.route('/getprofname',methods=['POST'])
def getname():
    if request.method != 'POST':
        return 
    dic={'name':course_eval_obj.getprofname(request.json['body'][0])}
    return json.dumps(dic)

@app.route('/getdepartment',methods=['GET'])
def getdepartment():
    if request.method != 'GET':
        return 
    dic={'name':course_eval_obj.getdeptname()}
    return json.dumps(dic)

@app.route('/getgraph', methods=['POST','GET'])
def getgraph():
    if request.method != 'POST':
            return
    url = 'http://{0}:8000/umap'.format(servicename)
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
        t,r = course_eval_obj.get_radar_plotdetails(course)
        if r is None:
            continue
        data.append(radar(r=r,theta=t,name=course))
    return radardata(data=data).json()


@app.route('/getcourseGPAgraph', methods=['POST','GET'])
def getGPAgraph():
    if request.method != 'POST':
            return
    string = request.json['body'][0]
    data=course_eval_obj.get_GPA_details(string)
    return radardata(data=data).json()


@app.route('/getinstrradar',methods=['POST','GET'])
def getinstrradar():
    if request.method != 'POST':
        return
    string = request.json['body'][0]
    data = []
    r,t = course_eval_obj.get_instr_details(string)
    data.append(radar(r=r,theta=t,name=string))
    #print(radardata(data=data).json())
    return radardata(data=data).json()

@app.route('/getinstrgradegraph', methods=['POST','GET'])
def getinstrgradegraph():
    if request.method != 'POST':
            return
    string = request.json['body'][0]
    data=course_eval_obj.get_instr_course_info(string)
    return radardata(data=data).json()

@app.route('/getplanner',methods=['POST'])
def get_planner():
    if request.method == 'POST':
        url = 'http://{0}:8000/plan'.format(servicename)
        data = request.json['body']
        for course in data:
            course['Time']=float(course['Time'])
            course['GPA_Actual']=float(course['GPA_Actual'])
            course['Recommend_Course']=float(course['Recommend_Course'])
            course['Rcmnd_Instr']=float(course['Rcmnd_Instr'])
            course['department']=course['department'].split(",")
        x = requests.post(url, data = json.dumps(data))
        data=[]
        #print(x.json())
        for i in x.json():
            #print(i)
            dic={}
            course_name=[]
            course_desp=[]
            gpa=[]
            time=[]
            for coursename,values in i.items():
                if coursename == 'cgpa':
                    continue
                course_name.append(coursename)
                course_desp.append(values['keyword'])
                time.append(round(values['Time'],2))
                gpa.append(round(values['GPA_Actual'],2))
            dic['data']=[course_name,gpa,time,course_desp]
            data.append(dic)

                
        '''
        dic={}
        dic['data']=[list(x.json()['recommend_set'][request.json['body'][0]]['courses'].keys()),
                    list(x.json()['recommend_set'][request.json['body'][0]]['courses'].values())]
        '''
        return json.dumps(data)
       

@app.route('/get_filter', methods=['POST','GET'])
def get_filter():
    data = request.json
    letter = data['letter'].strip()
    gpa = data['gpa'].strip()
    time = data['time'].strip()
    rec_class = data['rec_class'].strip()
    rec_instr = data['rec_instr'].strip()
    dep = data['dep'].strip().split(",")

    df = filter_obj.run(letter=letter, gpa=gpa, time=time, rec_class=rec_class, rec_instr=rec_instr, dep=dep)[['instr', 'course', 'term', 'rcmnd_class', 'rcmnd_instr', 'time', 'letter_actual', 'gpa_actual']]
    html_data = df.reset_index(drop=True).to_html(table_id="filter_table")

    return FilterHtmlData(table=html_data).json()

    