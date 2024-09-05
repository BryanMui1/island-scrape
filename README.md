# island-scrape

island-scrape is a scraping tool built for the statistical simulation website The Islands(https://islands.smp.uq.edu.au/login.php), it is a python script that allows researchers to automate sample collection. 

Collecting research samples from people:  
![Collecting research samples from people](https://github.com/user-attachments/assets/ce564d7f-a93b-4b9a-9dd2-d892f7cdfdcb)

Map of the entire Island: There's a lot of cities and people!  
![Map of the entire Island: There's a lot of cities and people!](https://github.com/user-attachments/assets/ab4bc1ce-92de-4c95-96b2-a75467515f53)

## Features include:  
+ ### sample.py - automated sample choosing and collection
+ ### collect.py - automated collection of experiment results
+ ### cache.py - caching script that makes data collection exponentially faster

# Instructions:

1) clone this respository  
2) install dependencies(requirements.txt) or manually installing the requirements listed here:  
```
pip install selenium
pip install numpy
pip install pandas
```
You also will need Google Chrome installed on the pc 

3) create a passwords.config file(look at sample-passwords.config for instructions)
4) generate a cache file by running cache.py
```
python cache.py
```  
the file should be stored in a binary file called **cache**

5) In sample.py edit the ##TASK## code for your specific size, and edit the SAMPLE_SIZE constant and run it using:
```
python sample.py
```  
Outputs a **sample_index** csv file that notes the indices of the people that you sampled

6) collect the data by editing the data collection script collect.py. change the ###DO SOMETHING### block to your choosing and run it using:
```
python collect.py
```  
Visits every person sampled, collects the data and outputs it into a csv file

The data will be outputed into a file named **"data1.csv"** or can be chaneged to your choosing


## Outlines of this project:
+ scrape.py: building block instances that can navigate through the page
+ iter.py: navigates through a population on the islan and performs some task(that you implement)
+ scrath.py: development file for temporary code
+ login.py: building block for logging into the website
+ **cache.py, sample.py, sample.py** finalized working scripts for *fast* sampling and data collection
+ iter.py: basic iteration instance over all cities 
+ scrape.py: used for testing one instance of scraping your data collection task
+ test.py: a combination of scrape.py and iter.py


Potential updates(in the future):
+ A script that navigates through one's island contact list
+ A script that adds all your samples to a contact list 
+ A script that allows randomization of experiments 

**This project was built using Selenium and Python3, and works with the integrated Chrome Web Driver**
