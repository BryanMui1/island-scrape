#!/usr/bin/env python3

### sample code that introduces the foundation to build loopable scripts for testing and navigation of the islands experiment simulator

################################################################################################################
## IMPORTS
################################################################################################################


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time

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

#exit()

################################################################################################################
## FIND CITY BUTTONS 
################################################################################################################

cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
num_cities = len(cities)

# for i in cities:
#     print(i.text)

buttons = []
for j in cities:
    buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "town town")]'))
    
# for button in buttons:
#     print("found " + button.text)

################################################################################################################
## FIND CITY BUTTONS 
################################################################################################################


#for i in range(num_cities):

buttons[0].click()
driver.implicitly_wait(1)

houses = driver.find_elements(By.CLASS_NAME, "house")
#print(len(houses))


# for house in houses:
#     id = house.find_element(By.CLASS_NAME, "houseid")
#     print(id.text)

ids = driver.find_elements(By.CLASS_NAME, "houseid")
#print(len(ids))

# for id in ids:
#     print(id.text)

### example of clicking on a house
#houses[23].click()

################################################################################################################
## SCRAPE RESIDENT INFORMATION
################################################################################################################

### get rid of bad indices
indx = []
for i in range(len(ids)):
    txt = ids[i].text
    if len(txt) == 0 or not txt.isnumeric():
        indx.append(i)

### get the good indices
indxgood = list(range(0, len(ids)))

for i in sorted(indx, reverse=True):
    indxgood.pop(i)

# for j in indxgood:
#     print(j)

actions = ActionChains(driver)

for i in indxgood:
    houses = driver.find_elements(By.CLASS_NAME, "house")
    houses[i].click()
    person = driver.find_element(By.XPATH, '//label[starts-with(@class, "modal__close")]')
    
    residents = driver.find_elements(By.XPATH, '//a[starts-with(@href, "islander.php")]')
    houseinfo = driver.find_element(By.ID, 'houseinfo')

    print(houseinfo.text)
    for j in range(len(residents)):
        residents = driver.find_elements(By.XPATH, '//a[starts-with(@href, "islander.php")]') 
        residents[j].click()
        driver.back()
        

    actions.move_to_element(person).click().perform()



#update clean ids and clean houses


# print(len(ids))
# print(len(houses))
# for i in ids:
#     print(i.text)


# for i in sorted(indexes, reverse=True):
#     list.pop(i)

#click on the numbers, find the x button,

time.sleep(10)

driver.quit()