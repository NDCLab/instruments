from subscore import Subscore

import pandas as pd
import regex as re


class Survey:
    """Class that utilizes Subscore class to score all available subscores.

    Instance Variables
    ----------
    name:   str | None
            String that contains the survey name.
    versions:   list | None
                List that contains survey versions if listed. Initialized in _extract_versions(). 
    file_name:  str
                Filename that contains csv survey data.
    data:    pd.Dataframe
             Pandas dataframe that contains csv data. Created from private method _load_data().
    subscores:  dict() | None
                Dictionary object containing all subscores and the parameters they go to.

                Ex: 
                {"subscore1": {
                        "select": [1, 2, 5],
                        "type": "sum"
                },
                "subscore2": {
                        "select": [3, 4, 6, 10, 14],
                        "type": "avg"
                }}

                Alternatively, None if no subscores available.
    
    Private Methods
    ----------
    _filter(self):
            Firstly checks if subscores exist. Filter out non-survey data based on self.name, 
            called in init.
    _extract_versions(self):
            Extracts survey versions if available, called in init.
    _load_data(self):
            Use self.file_name to init pandas dataframe and returns.

    Public Methods
    ----------
    score(self):
            Function to iterate and score over all subscores, and generate dataframe containing 
            all subscores. Returns modified dataframe. 
    """
    VER_POS = 1
    SES_POS = -3
    RUN_POS = -2
    EVENT_POS = -1

    DELIM = Subscore.DELIM

    def __init__(self, name, file_name, subscores):
        self.name = name
        self.file_name = file_name
        self.subscores = subscores

        # init and filter data
        self.data = self._load_data()
        self._filter()

        # init default versions and extract potential versions
        self.versions = []
        self._extract_versions()
        
        # remove metadata
        self._remove_meta()

    def _load_data(self):
        # load filename into dataframe
        file = pd.read_csv(self.file_name, index_col="record_id")
        return file
        
    def _filter(self):
        if len(self.subscores) == 0:
            raise TypeError("Subscores for %s is empty. Skipping."%(self.name))
        # keep only survey data containing survey name
        self.data = self.data.filter(regex=rf"^{self.name}")
        # quit processing if survey data is not available 
        if(self.data.empty):
            raise RuntimeError("Data does not contain %s survey data. Skipping."%(self.name))

        # Drop rows with incomplete values in timestamp (indicating no data)
        timestamp_col = self.data.filter(regex=rf"_{Subscore.TIME_LABEL}").columns
        self.data.dropna(subset=timestamp_col, how='all', inplace=True)
        if(self.data.empty):
            raise RuntimeError("Survey %s does not contain any values. Skipping."%(self.name))
    
    def _extract_versions(self):
        # init regex
        surv_reg = rf"{self.name}"
        ver_reg = rf"{self.name}_[a-z]*_"

        # get timestamp column of all versions
        timestamp_col = self.data.filter(regex=rf"_{Subscore.TIME_LABEL}").columns
        # extract potential versions using timestamp
        for ver in timestamp_col:
            surv_res = re.search(surv_reg, ver)
            ver_res = re.search(ver_reg, ver)
            if ver_res is not None:
                if ver_res.group(0)[:-1] not in self.versions:
                    self.versions.append(ver_res.group(0)[:-1])
            elif surv_res is not None:
                if surv_res.group(0) not in self.versions:
                    self.versions.append(surv_res.group(0))
        self.versions.sort()
        
                    
    def _remove_meta(self):
        metadata_col = self.data.filter(regex=rf"{self.DELIM}{Subscore.TIME_LABEL}|{self.DELIM}{Subscore.COMP_LABEL}").columns
        self.data = self.data.drop(metadata_col, axis=1)
        
    def score(self):
        # Iterate through versions then subscores and score on data
        all_scores = pd.DataFrame()
        for ver_surv in self.versions:
            ver_scores = pd.DataFrame()
            product_scores = pd.DataFrame()
            for subscore, params in self.subscores.items():
                if len(params) == 0:
                    raise TypeError("No parameters for %s. Skipping."%(subscore))
                try:
                    sub_obj = Subscore(name=ver_surv, sub_name=subscore, **params)
                    if sub_obj.products == None:
                        single_score = sub_obj.gen_data(self.data.filter(regex=rf"{ver_surv}_[a-z][0-9]"))
                        ver_scores = pd.concat([ver_scores, single_score], axis=1)
                    else:
                        product_score = sub_obj.gen_data_for_products(ver_scores)
                        product_scores = pd.concat([product_scores, product_score], axis=1)
                        ver_scores = pd.DataFrame()
                except RuntimeError:
                    continue
             # Sort according to session, run, and event, in that order
            product_scores = product_scores.reindex(
                sorted(product_scores.columns, key=lambda x: \
                    (int(x.split(self.DELIM)[self.SES_POS][1]),\
                    int(x.split(self.DELIM)[self.RUN_POS][1]),\
                    int(x.split(self.DELIM)[self.EVENT_POS][1]))\
            ), axis=1)
            all_scores = pd.concat([all_scores, product_scores], axis=1)

            # Sort according to session, run, and event, in that order
            ver_scores = ver_scores.reindex(
                sorted(ver_scores.columns, key=lambda x: \
                    (int(x.split(self.DELIM)[self.SES_POS][1]),\
                    int(x.split(self.DELIM)[self.RUN_POS][1]),\
                    int(x.split(self.DELIM)[self.EVENT_POS][1]))\
            ), axis=1)
            all_scores = pd.concat([all_scores, ver_scores], axis=1)
        
        return all_scores

