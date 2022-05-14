# Import library
from bs4 import BeautifulSoup
import requests
import pandas as pd
'''
Extraction course descriptions for History department
'''
# Define URL
url = 'https://catalog.ucsd.edu/courses/HIST.html'
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
# 
course_descriptions_list=course_descriptions_list[4:]
# print(course_descriptions_list[20:60])

name=course_descriptions_list.pop(38)
name=course_descriptions_list.pop(48)
name=course_descriptions_list.pop(112)
name=course_descriptions_list.pop(271)
name=course_descriptions_list.pop(375)
name=course_descriptions_list.pop(445)
name=course_descriptions_list.pop(501)
name=course_descriptions_list.pop(573)
name=course_descriptions_list.pop(732)
name=course_descriptions_list.pop(772)
name=course_descriptions_list.pop(138)
name=course_descriptions_list.pop(604)
# for i in course_descriptions_list:
#     if i.startswith("See"):
#         print(course_descriptions_list.index(i))
name=course_descriptions_list.pop(-1)
# print(course_descriptions_list[-1])

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
# print(len(course_list),len(description_list),len(prerequisite_list))
df_hist = pd.DataFrame({'Course_Name':course_list,
'Course_Description':description_list,
'Prerequisites':prerequisite_list})
# print(df_hist.head())
df_hist.to_csv("D:\ECE_229\ECE229_Project\data_history.csv")