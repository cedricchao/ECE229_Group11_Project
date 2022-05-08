# Import library
from bs4 import BeautifulSoup
import requests
import pandas as pd
# Define URL
url = 'https://catalog.ucsd.edu/courses/NANO.html'
# Ask hosting server to fetch url
requests.get(url)
pages = requests.get(url)
# parser-lxml = Change html to Python friendly format
soup = BeautifulSoup(pages.text, 'lxml')
course_descriptions=soup.find_all('p')
course_descriptions_list = []
for i in course_descriptions:
    descriptions = i.text
    descriptions=descriptions.replace("\xa0",'')
    if descriptions!='':
        course_descriptions_list.append(descriptions)
course_descriptions_list=course_descriptions_list[4:]
name=course_descriptions_list.pop(175)
name=course_descriptions_list.pop(-1)
course_list=[]
description_list=[]
prerequisite_list=[]
# print(type(course_descriptions))
for i in range(len(course_descriptions_list)):
    # print(i)
    if i%2==0:
        # print(i)
        course_list.append(course_descriptions_list[i])
for i in range(len(course_descriptions_list)):
    if i%2!=0:
        if 'Prerequisites:' in course_descriptions_list[i]:
            text_list=course_descriptions_list[i].split("Prerequisites:")
            description_list.append(text_list[0])
            prerequisite_list.append(text_list[1])
        else:
            description_list.append(course_descriptions_list[i])
            prerequisite_list.append('')
print(len(course_list),len(description_list),len(prerequisite_list))
df_nano = pd.DataFrame({'Course_Name':course_list,
'Course_Description':description_list,
'Prerequisites':prerequisite_list})
print(df_nano.head())
df_nano.to_csv("D:\ECE_229\ECE229_Project\data_nanoengg.csv")