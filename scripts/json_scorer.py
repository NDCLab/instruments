import json
from survey import Survey
import pandas as pd

import sys


def score_tracker(output_data, scrd_columns, tracker):
    """
    Code to load in pandas dataframe of scored data and update tracker
    Parameters
    ----------
    output_data:    pd.df()
                    Dataframe containing scored surveys 
    scrd_columns:   list
                    list of columns to be check 
    tracker:    str 
                String pointing to tracker file. To be overwritten
    """
    tracker_df = pd.read_csv(tracker, index_col="id")

    for index, row in file_df.iterrows():
        id = row.name
        # check if id exists in tracker
        if id not in tracker_df.index:
            print(id, "missing in tracker file, skipping")
            continue
        for col in scrd_columns:
            try:
                val = file_df.loc[id, key]
                if val >= 10:
                    continue
                tracker_df.loc[id, key] = 11 if val != "NA" else 19
            except Exception as e_msg:
                tracker_df.loc[id, key] = 0

    tracker_df.to_csv(data_tracker_file)
    print("Success: data tracker updated.")



def json_score(input_path, survey_dat, output_path=None, tracker=None):
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
    scrd_columns = []
    for name, subscores in survey_dat.items():
        # Try to score, continue if fails
        try:
            survey_obj = Survey(name, input_path, subscores)
            handle = survey_obj.score()
            # collect all columns from handle that contains "scrd"
            scrd_columns += [col for col in list(data.columns) if "scrd" in col]
            all_surveys = pd.concat([all_surveys, handle], axis=1)
        except RuntimeError:
            continue
    all_surveys.fillna(value="NA", inplace=True)

    if output_path is not None:  
        all_surveys.to_csv(output_path)

    if tracker is not None:
        score_tracker(all_surveys, scrd_columns, tracker)

    return all_surveys
    
if __name__ == "__main__":
    input =  sys.argv[1]
    json_data = sys.argv[2]
    out_path = sys.argv[3]

    # specify optional tracker to read over scored data and update specified data tracker
    tracker = sys.argv[4]

    json_score(input, json_data, out_path, tracker)
