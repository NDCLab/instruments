import json
from instruments.survey import Survey
import pandas as pd

import sys

"""
Code to load in JSON file and score outlined surveys.
Simply run and get output! 

Output will be labeled "data/outputs/<survey_name>_data.csv"
"""

input = sys.argv[1]
out_path = sys.argv[2]

# Open and save survey data
with open('surveys.json','r') as infile:
    surveys = json.load(infile)

# Iterate through survey names and generate data
all_surveys = pd.read_csv(input, index_col="record_id")
for name, subscores in surveys.items():
    survey_obj = Survey(name, input, subscores)
    handle = survey_obj.score()
    all_surveys = pd.concat([all_surveys, handle], axis=1)
all_surveys.fillna(value="N/A", inplace=True)
all_surveys.to_csv(out_path + "/output.csv")