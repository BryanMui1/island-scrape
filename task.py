#!/usr/bin/env python3

# Example Task function that looks for the first person's profile and dumps out basic information about their name, age, village, etc.

################################################################################################################
## IMPORTS
################################################################################################################


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time

import numpy as np
import pandas as pd

################################################################################################################
## LOGIN
################################################################################################################

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://islands.smp.uq.edu.au/login.php")

#driver.implicitly_wait(1)

email = driver.find_elements(by=By.TAG_NAME, value="input")

login = open('passwords.config', 'r')
usrpass = [line.rstrip('\n') for line in login]


email[0].send_keys(usrpass[1])
email[1].send_keys(usrpass[2])

email[2].click()

logURL = "https://islands.smp.uq.edu.au/index.php"

assert(driver.current_url == logURL)

################################################################################################################
## GET TO HOUSE
################################################################################################################

cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
num_cities = len(cities)

buttons = []
for j in cities:
    buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "town town")]'))

buttons[1].click()

houses = driver.find_elements(By.CLASS_NAME, "house")
ids = driver.find_elements(By.CLASS_NAME, "houseid")

houses[100].click()

driver.implicitly_wait(3)

residents = driver.find_elements(By.XPATH, '//a[starts-with(@href, "islander")]')
houseinfo = driver.find_element(By.ID, 'houseinfo')

residents[0].click()

################################################################################################################
## TASK
################################################################################################################

driver.implicitly_wait(3)
summary = driver.find_elements(By.XPATH, '//tr')
header = driver.find_element(By.CLASS_NAME, "crumb").text.split()
name = header[1] + " " + header[2]


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


for element in summary: print(element.text)


age = summary[1].text.split()[0]

temp = 0
while summary[temp].text != "Parents":
    if summary[temp].text.find("$") != -1:
        income = summary[temp].text[1:].replace(',', '')
    if summary[temp].text.find("Lives in") != -1:
        location = summary[temp].text.split()
        island = location[2]
        housenum = location[3]
    temp+=1


print(name)
print(age)
print(income)
print(island)
print(housenum)

agevec = []
incomevec = []
namevec = []
islandvec = []
housenumvec = []
educationvec = []

namevec.append(name)
agevec.append(age)
incomevec.append(income)
islandvec.append(island)
housenumvec.append(housenum)
educationvec.append(get_education())


data = pd.DataFrame(
    {
        "name": namevec,
        "age": agevec,
        "gender": "unknown",
        "island": islandvec,
        "house": housenumvec,
        "education_level": educationvec,
        "iq": "unknown",
        "income": incomevec,
    }
)

print(data.head())



if __name__ == '__main__':
    time.sleep(15)
    driver.close()
