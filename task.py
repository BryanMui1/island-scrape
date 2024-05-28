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

buttons[0].click()

houses = driver.find_elements(By.CLASS_NAME, "house")
ids = driver.find_elements(By.CLASS_NAME, "houseid")

houses[0].click()

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

tmp = 0
for element in summary:
    print(str(tmp) + " " + element.text)
    tmp+=1
    

age = summary[1].text.split()[0]
income = summary[3].text[1:].replace(',', '')
location = summary[4].text.split()
island = location[2]
housenum = location[3]

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

namevec.append(name)
agevec.append(age)
incomevec.append(income)
islandvec.append(island)
housenumvec.append(housenum)


data = pd.DataFrame(
    {
        "name": namevec,
        "age": agevec,
        "gender": "uknown",
        "island": islandvec,
        "house": housenumvec,
        "education_level": "idk",
        "iq": 120,
        "income": incomevec,
    }
)

print(data.head())

if __name__ == '__main__':
    time.sleep(15)
    driver.close()
