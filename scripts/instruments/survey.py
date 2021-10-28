from scripts.instruments.subscore import Subscore


class Survey:
    """Class that utilizes Subscore class to score all available subscores.
    By default if the subscores are empty, simply scores total score and returns.

    Instance Variables
    ----------
    name:   str
            String that contains the survey name
    data:   pandas.Dataframe()
            Dataframe that contains csv survey data
    subscores:  dict() 
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
    
    Private Methods
    ----------
    _filter(self):
            Filter out non-survey data based on self.name, called in init. 

    Public Methods
    ----------
    score_write(self, filename):
            Function to iterate and score over all subscores, and write csv containing all subscores to filename.
            Modifies original data in place, and returns modified dataframe. 
    """
    def __init__(self, name, data, subscores):
        self.name = name
        self.data = data
        self.subscores = subscores

        # Once data is initialized, filter out irrelevant data
        self._filter(self.data, self.name)
    
    def _filter(self, data, name):
        # keep only the relevant survey data
        data = data.filter(regex=rf"{name}_")

        # Drop columns with incomplete values in timestamp
        timestamp_col = data.filter(regex=rf"_{Subscore.TIME_LABEL}").columns
        data.dropna(subset=timestamp_col, inplace=True)
        return data
    
    def score_write(self, filename):
        default = Subscore()
        scored_total_data = default.get_data(self.data)
        # If no subscores, return default total
        if not len(self.subscores):
            # Write out to filename and return
            scored_total_data.to_csv(filename)
            return scored_total_data
        for subscore, params in self.subscores.items():
            sub_obj = Subscore(name=subscore, **params)
            subscored_data = sub_obj.get_data(self.data)
        return subscored_data
