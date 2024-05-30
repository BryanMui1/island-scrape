#!/usr/bin/env python3

import pickle

cache_file = open(r'cache', 'rb')
cache = pickle.load(cache_file)
cache_file.close()

print(len(cache))

exit()

import numpy as np

rand = np.random.randint(1, high=10, size=10)

print(rand)

name_vec = []
age_vec = []
gender_vec = []
island_vec = []
house_num_vec = []
education_vec = []
iq_vec = []
income_vec = []

################################################################################################################
## TASK
################################################################################################################

# initialize vars
name = "NA"
age = 0
gender = "NA"
income = 0
island = "NA"
housenum = 0
education_level = "NA"
iq = 0
income = 0

### format 
'''
    "name": namevec,
    "age": agevec,
    "gender": gendervec,
    "island": islandvec,
    "house": housenumvec,
    "education_level": educationvec,
    "iq": "iqvec,
    "income": incomevec,
'''

summary = driver.find_elements(By.XPATH, '//tr')
header = driver.find_element(By.CLASS_NAME, "crumb").text.split()
########## define name
name = header[1] + " " + header[2]

########## define education_level
## function to find a person's education status
def get_education():
    summary_string = ''
    for element in summary:
        summary_string += " " + element.text

    if summary_string.find("University") != -1:
        return "university"
    elif summary_string.find("High School") != -1:
        return "high school"
    elif summary_string.find("Elementary School") != -1:
        return "elementary school"
    else:
        return "none"
education_level = get_education() 

########## define age
age = summary[1].text.split()[0]


########## define income, island, housenum
temp = 0
while not summary[temp].text.isspace():
    if summary[temp].text.find("$") != -1:
        income = summary[temp].text[1:].replace(',', '')

    if summary[temp].text.find("Lives in") != -1:
        location = summary[temp].text.split()
        island = location[2]
        housenum = location[3]
    temp+=1

########## define gender

########## define iq

#print(name + " " + str(age) + " " + str(income) + " " + island + " " + str(housenum) + " " + get_education())      

namevec.append(name)
agevec.append(age)
incomevec.append(income)
islandvec.append(island)
housenumvec.append(housenum)
educationvec.append(get_education())