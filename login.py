#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

################################################################################################################
## LOGIN
################################################################################################################

def login():
    chrome_options = Options()
    
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://islands.smp.uq.edu.au/login.php")

    email = driver.find_elements(by=By.TAG_NAME, value="input")

    login = open('passwords.config', 'r')
    usrpass = [line.rstrip('\n') for line in login]

    email[0].send_keys(usrpass[1])
    email[1].send_keys(usrpass[2])

    email[2].click()

    logURL = "https://islands.smp.uq.edu.au/index.php"

    assert(driver.current_url == logURL)

    return driver

if __name__ == '__main__':
    login()