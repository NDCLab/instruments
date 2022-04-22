import json
from survey import Survey
import pandas as pd

import sys


def json_score(input_path, survey_dat, output_path=None):
    """
    Code to load in JSON file and score outlined surveys. Returns scored data joined with data.
    Writes to output_path if specified
    Parameters
    ----------
    input_path: str
                String pointing to input data
    survey_dat: str | dict
                Dictionary or path to json containing survey names and parameters
    output_path:    str | None
                    string pointing to output path and name. None if data should not be written out
    """
    # Open and save survey data
    if (isinstance(survey_dat, str)):
        with open(survey_dat,'r') as infile:
            survey_dat = json.load(infile)

    # Iterate through survey names and generate data
    all_surveys = pd.read_csv(input_path, index_col="record_id")
    for name, subscores in survey_dat.items():
        # Try to score, continue if fails
        try:
            survey_obj = Survey(name, input_path, subscores)
            handle = survey_obj.score()
            all_surveys = pd.concat([all_surveys, handle], axis=1)
        except RuntimeError:
            continue
    all_surveys.fillna(value="N/A", inplace=True)
    if output_path is not None:  
        all_surveys.to_csv(output_path)
    return all_surveys
    
if __name__ == "__main__":
    input =  sys.argv[1]
    json_data = sys.argv[2]
    out_path = sys.argv[3]

    json_score(input, json_data, out_path)
