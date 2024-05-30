#!/usr/bin/env python3

'''
Random Sampling Function:
- Choose a random city, a random house, and a random person 
- If the person isnt a working class citizen(age 15 to 64), then redraw
- If participant declines, then redraw
- obtain n = 220 samples
'''

################################################################################################################
## IMPORTS
################################################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import numpy as np
import pandas as pd

import time
import datetime

start_time = time.time()

################################################################################################################
## LOGIN
################################################################################################################

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://islands.smp.uq.edu.au/login.php")

driver.implicitly_wait(1)

email = driver.find_elements(by=By.TAG_NAME, value="input")

login = open('passwords.config', 'r')
usrpass = [line.rstrip('\n') for line in login]


email[0].send_keys(usrpass[1])
email[1].send_keys(usrpass[2])

email[2].click()

logURL = "https://islands.smp.uq.edu.au/index.php"

assert(driver.current_url == logURL)

################################################################################################################
## ENUMERATE CONSTANTS AND GLOBAL VARS(LOAD INDEX DATA TOO)
################################################################################################################

# making dataframe  
df = pd.read_csv("sample_index.csv") 
city_index = df['city_index']
sample_index = df['sample_index']
person_index = df['person_index']

SAMPLE_SIZE = len(df)
people_sampled = 0

cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
NUM_CITIES = len(cities)

buttons = []
for j in cities:
    buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "town town")]'))

assert(len(buttons) == NUM_CITIES)

# make data vectors
name_vec = []
age_vec = []
gender_vec = []
island_vec = []
house_num_vec = []
education_vec = []
iq_vec = []
income_vec = []

################################################################################################################
## RUNTIME BODY
################################################################################################################

for df_count in range(0, SAMPLE_SIZE):

    ## window check 1
    # Store the ID of the original window
    original_window = driver.current_window_handle

    # Loop through until we find a new window handle
    if driver.current_window_handle == original_window and len(driver.window_handles) > 1:
        driver.close()

    driver.switch_to.window(driver.window_handles[0])

    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1
    driver.implicitly_wait(3)

    #reprocess island page
    cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
    buttons = []
    for j in cities:
        buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "towndot towndot")]'))
    click_btn = ActionChains(driver)
    click_btn.move_to_element(buttons[city_index[df_count]])
    click_btn.click()
    click_btn.perform()
    
    ## window check 2
    # Store the ID of the original window
    original_window = driver.current_window_handle

    # Loop through until we find a new window handle
    if driver.current_window_handle == original_window and len(driver.window_handles) > 1:
        driver.close()

    driver.switch_to.window(driver.window_handles[0])

    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1
    driver.implicitly_wait(3)    
   

    ### PERFORM SOME TASK HERE ###

    ################################################################################################################
    ## ENUMERATE INDICES
    ################################################################################################################

    houses = driver.find_elements(By.CLASS_NAME, "house")

    ids = driver.find_elements(By.CLASS_NAME, "houseid")
 
    ################################################################################################################
    ## SCRAPE RESIDENT INFORMATION
    ################################################################################################################


    actions = ActionChains(driver)
    ctrl_click = ActionChains(driver)

    # open the desired house

    houses[sample_index[df_count]].click()
 
    ##### TASK START #####

    # initialize vars
    name = "NA"
    age = 0
    gender = "NA"
    island = "NA"
    house_num = 0
    education_level = "NA"
    iq = 0
    income = 0

    ### format 
    '''
        "name": name_vec,
        "age": age_vec,
        "gender": gender_vec,
        "island": island_vec,
        "house_num": house_num_vec,
        "education_level": education_vec,
        "iq": "iq_vec,
        "income": income_vec,
    '''

    ## open person
    resident_links = driver.find_elements(By.XPATH, '//a[starts-with(@href, "islander.php")]')
    num_residents = len(resident_links)

    resident_links[person_index[df_count]].click()
    tab = driver.find_element(By.ID, "t1tab")
    tab.click()
    driver.implicitly_wait(1)

        ### Perform Data Collection ###
    isl = driver.find_element(By.ID, "title")
    print("touched " + isl.text)

    summary = driver.find_elements(By.XPATH, '//tr')
    driver.implicitly_wait(1)
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
            house_num = location[3]
        temp+=1

    ########## define iq
    tab = driver.find_element(By.ID, "t2tab")
    tab.click()

    driver.implicitly_wait(3)
 
    iq = driver.find_elements(By.CLASS_NAME, "taskresultresult")[0].text

    ########## define gender
    tab = driver.find_element(By.ID, "t3tab")
    tab.click()
    chatbox = driver.find_element(By.ID, "chatbox")
    chatbox.send_keys("Are you male or female?")
    submit_chat = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_chat.click()
    driver.implicitly_wait(3)

    response = driver.find_elements(By.CLASS_NAME, "chatbot")[-1].text
    if response == "I am male.":
        gender = "male"
    if response == "I am female.":
        gender = "female"
    else:
        print("gender failed.")


    # append the data
    name_vec.append(name)
    age_vec.append(age)
    gender_vec.append(gender)
    island_vec.append(island)
    house_num_vec.append(house_num)
    education_vec.append(education_level)
    iq_vec.append(iq)
    income_vec.append(income)


         ### Done Data Collection ###

  
  
    ##### TASK END #####

    ### DONE

    ### close window 
    #driver.switch_to.window(driver.window_handles[0])
    # close = driver.find_element(By.XPATH, '//label[starts-with(@class, "modal__close")]')
    # actions.move_to_element(close).click().perform()
    # driver.implicitly_wait(3)

    ### END TASK//

    island_home = driver.find_element(By.CLASS_NAME, "menu")
    island_home.click()
    driver.implicitly_wait(3)
## Create data frame and write to csv

data = pd.DataFrame(
    {
        "name": name_vec,
        "age": age_vec,
        "gender": gender_vec,
        "island": island_vec,
        "house_num": house_num_vec,
        "education_level": education_vec,
        "iq": iq_vec,
        "income": income_vec,
    }
)

print(data.head())

data.to_csv('data1.csv')


end_time = time.time()

if __name__ == '__main__':
    execution_time = end_time - start_time
    print("Script completed normally.")
    print("Script runtime: " + str(datetime.timedelta(seconds=execution_time)))

    time.sleep(10)
    driver.close()