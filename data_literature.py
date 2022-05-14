# Import library
from bs4 import BeautifulSoup
import requests
import pandas as pd
'''
Extraction course descriptions for Literature department
'''
# Define URL
url = 'https://catalog.ucsd.edu/courses/LIT.html'
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
# print(course_descriptions_list[:10])
# print(course_descriptions_list[20:60])

name=course_descriptions_list.pop(4)
name=course_descriptions_list.pop(20)
name=course_descriptions_list.pop(22)
name=course_descriptions_list.pop(49)
name=course_descriptions_list.pop(94)
name=course_descriptions_list.pop(110)
name=course_descriptions_list.pop(172)
name=course_descriptions_list.pop(268)
name=course_descriptions_list.pop(300)
name=course_descriptions_list.pop(330)
name=course_descriptions_list.pop(336)
name=course_descriptions_list.pop(364)
name=course_descriptions_list.pop(370)
name=course_descriptions_list.pop(376)
name=course_descriptions_list.pop(392)
name=course_descriptions_list.pop(396)
name=course_descriptions_list.pop(402)
name=course_descriptions_list.pop(416)
name=course_descriptions_list.pop(426)
name=course_descriptions_list.pop(454)
name=course_descriptions_list.pop(460)
name=course_descriptions_list.pop(466)
name=course_descriptions_list.pop(490)
name=course_descriptions_list.pop(491)
name=course_descriptions_list.pop(510)
name=course_descriptions_list.pop(511)
name=course_descriptions_list.pop(522)
name=course_descriptions_list.pop(592)
name=course_descriptions_list.pop(602)
name=course_descriptions_list.pop(603)
name=course_descriptions_list.pop(604)
name=course_descriptions_list.pop(612)
name=course_descriptions_list.pop(624)
name=course_descriptions_list.pop(628)
name=course_descriptions_list.pop(722)
name=course_descriptions_list.pop(723)
name=course_descriptions_list.pop(724)
name=course_descriptions_list.pop(760)
name=course_descriptions_list.pop(778)

# for i in course_descriptions_list:
#     if i.startswith("LTWR 215"):
#         print(course_descriptions_list.index(i))
name=course_descriptions_list.pop(-1)
# print(course_descriptions_list[-1])
# print(course_descriptions_list[758:762])
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
df_lit = pd.DataFrame({'Course_Name':course_list,
'Course_Description':description_list,
'Prerequisites':prerequisite_list})
# print(df_hist.head())
df_lit.to_csv("D:\ECE_229\ECE229_Project\data_literature.csv")