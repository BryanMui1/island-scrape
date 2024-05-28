#!/usr/bin/env python3

# Test script to retrieve population data on Vardo

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
## ENUMERATE CONSTANTS AND GLOBAL VARS
################################################################################################################

cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
NUM_CITIES = len(cities)

buttons = []
for j in cities:
    buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "town town")]'))

assert(len(buttons) == NUM_CITIES)

agevec = []
incomevec = []
namevec = []
islandvec = []
housenumvec = []
educationvec = []

################################################################################################################
## RUNTIME BODY
################################################################################################################

for cityindex in range(5):
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
    click_btn.move_to_element(buttons[cityindex])
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
    isl = driver.find_element(By.ID, "title")
    print("touched " + isl.text)

    ################################################################################################################
    ## ENUMERATE INDICES
    ################################################################################################################

    houses = driver.find_elements(By.CLASS_NAME, "house")

    ids = driver.find_elements(By.CLASS_NAME, "houseid")

    ### get rid of bad indices
    badindx = []
    for i in range(len(ids)):
        txt = ids[i].text
        if len(txt) == 0 or not txt.isnumeric():
            badindx.append(i)

    ### get the good indices
    indxgood = list(range(0, len(ids)))

    for i in sorted(badindx, reverse=True):
        indxgood.pop(i)

    ################################################################################################################
    ## SCRAPE RESIDENT INFORMATION
    ################################################################################################################

    ## Task 2: Touch every person's profile

    # error checking: keep track of house num and people touched
    pop_total = 0
    people_touched = 0

    actions = ActionChains(driver)
    ctrl_click = ActionChains(driver)
    for i in indxgood[0:5]:
        # open the desired house
        houses = driver.find_elements(By.CLASS_NAME, "house")
        houses[i].click()
        driver.implicitly_wait(1)
        
        ### DO SOMETHING

        ## open the every person in the house
        resident_links = driver.find_elements(By.XPATH, '//a[starts-with(@href, "islander.php")]')
        num_residents = len(resident_links)
        pop_total+=num_residents
        for n in range(num_residents):
            ctrl_click.move_to_element(resident_links[n])
            ctrl_click.key_down(Keys.CONTROL)
            ctrl_click.click()
            ctrl_click.perform()

        for _ in range(num_residents):
            driver.implicitly_wait(1)
            driver.switch_to.window(driver.window_handles[-1])
            
            ### paste in task here ###

            ### touch the person ###
            isl = driver.find_element(By.ID, "title")
            people_touched+=1

            ################################################################################################################
            ## TASK
            ################################################################################################################

            # initialize vars
            name = "NA"
            age = 0
            income = 0
            island = "NA"
            housenum = 0
            

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

            age = summary[1].text.split()[0]

            temp = 0
            while not summary[temp].text.isspace():
                if summary[temp].text.find("$") != -1:
                    income = summary[temp].text[1:].replace(',', '')
            
                if summary[temp].text.find("Lives in") != -1:
                    location = summary[temp].text.split()
                    island = location[2]
                    housenum = location[3]
                temp+=1

            print(name + " " + str(age) + " " + str(income) + " " + island + " " + str(housenum) + " " + get_education())      

            namevec.append(name)
            agevec.append(age)
            incomevec.append(income)
            islandvec.append(island)
            housenumvec.append(housenum)
            educationvec.append(get_education())


            ##### TASK END #####

            driver.close()
        ## move to the next house

        ### DONE

        ### close window 
        driver.switch_to.window(driver.window_handles[0])
        close = driver.find_element(By.XPATH, '//label[starts-with(@class, "modal__close")]')
        actions.move_to_element(close).click().perform()

    # assert error checking that we touched everyone
    print(people_touched)
    print(pop_total)

    assert(people_touched == pop_total)
    driver.implicitly_wait(3)

    ### END TASK//

    island_home = driver.find_element(By.CLASS_NAME, "menu")
    island_home.click()
    time.sleep(2)

## Create data frame and write to csv

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

data.to_csv('output.csv')


end_time = time.time()

if __name__ == '__main__':
    execution_time = end_time - start_time
    print("Script completed normally.")
    print("Script runtime: " + str(datetime.timedelta(seconds=execution_time)))
    time.sleep(15)
    driver.close()