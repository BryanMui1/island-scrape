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

import pickle

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
## ENUMERATE CONSTANTS AND GLOBAL VARS
################################################################################################################

SAMPLE_SIZE = 220
people_sampled = 0

cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
NUM_CITIES = len(cities)

buttons = []
for j in cities:
    buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "town town")]'))

assert(len(buttons) == NUM_CITIES)

city = [] #rng_city
housers = [] #SAMPLE_INDEX
persons = [] #rng_person

################################################################################################################
## LOAD CACHE
################################################################################################################

cache_file = open(r'cache', 'rb')
cache = pickle.load(cache_file)
cache_file.close()
# cache check assertion
assert(len(cache) == NUM_CITIES)

################################################################################################################
## RUNTIME BODY
################################################################################################################

while people_sampled < SAMPLE_SIZE:
    # generate a random city
    rng_city = np.random.randint(0, high=NUM_CITIES-1)

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
    click_btn.move_to_element(buttons[rng_city])
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

    ### find the number of houses 
    NUM_HOUSES = list(cache[rng_city].keys())[-1]
    setids = set(cache[rng_city].keys())

    ## choose a random house
    # check that the house is valid with people
    while True:
        rng_house = np.random.randint(1, high=NUM_HOUSES)
        if(str(rng_house) in setids):
            print("sample house " + str(rng_house))
            break
        else:
            print("Invalid House. resampling")    

    SAMPLE_INDEX = cache[rng_city][str(rng_house)]


    ##USELESS COMMENTS
    # print(setids)
    # rng = np.random.randint(1, high=NUM_HOUSES)
    # print(rng)
    # print(str(rng) in setids)
    # print("house num " + rnghouse)
    # print("index " + hashid)
 
    ################################################################################################################
    ## SCRAPE RESIDENT INFORMATION
    ################################################################################################################


    actions = ActionChains(driver)
    ctrl_click = ActionChains(driver)

    # open the desired house

    houses[SAMPLE_INDEX].click()
 
    ##### TASK START #####

    ## open a random person
    resident_links = driver.find_elements(By.XPATH, '//a[starts-with(@href, "islander.php")]')
    num_residents = len(resident_links)
    if num_residents == 0:
        print("empty house")
    else:
        if num_residents == 1:
            rng_person = 0
        else:
            rng_person = np.random.randint(low=0, high=num_residents-1)
        resident_links[rng_person].click()
        driver.implicitly_wait(1)



            ### Start Tasking ###
        isl = driver.find_element(By.ID, "title")
        print("touched " + isl.text)

        # check if their age is the right age range
        tab = driver.find_element(By.ID, "t1tab")
        tab.click()
        driver.implicitly_wait(3)
        
        summary = driver.find_elements(By.XPATH, '//tr')
        ########## define age
        age = int(summary[1].text.split()[0])

        if(age >= 15 and age <= 64):
            tab = driver.find_element(By.ID, "t2tab")
            tab.click()
            driver.implicitly_wait(3)
            obtain = driver.find_elements(By.ID, "obtain")
        
            if len(obtain) > 0:
                obtain = obtain[0].find_element(By.XPATH, '//a[starts-with(@href, "javascript:getConsent")]')
                obtain.click()
            
            task_result = driver.find_elements(By.CLASS_NAME, "taskresulttask")
            if(task_result[-1].text.find("consented") != -1):
                print("consented")
                # do something
                tasks_recent = driver.find_element(By.ID, "tasksrecent")
                iq_test = tasks_recent.find_element(By.XPATH, """//span[@onclick="startTask('iq'); return false;"]""")
                iq_test.click()

                city.append(rng_city) #rng_city
                housers.append(SAMPLE_INDEX) #SAMPLE_INDEX
                persons.append(rng_person) #rng_person

                people_sampled += 1
            else:
                print("Person declined. sample again")
        else:
            print("incorrect age. sample again")

            ### done touching people ###

  
  
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
        "city_index": city,
        "sample_index": housers,
        "person_index": persons,
    }
)

print(data.head())

data.to_csv('sample_index.csv')


end_time = time.time()

if __name__ == '__main__':
    execution_time = end_time - start_time
    print("Script completed normally.")
    print("Script runtime: " + str(datetime.timedelta(seconds=execution_time)))

    time.sleep(10)
    driver.close()