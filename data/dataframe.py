#!/usr/bin/env python3

# import pandas module  
import pandas as pd  
    
# making dataframe  
df = pd.read_csv("sample_index.csv") 
city_index = df['city_index']
sample_index = df['sample_index']
person_index = df['person_index']

print(len(df))