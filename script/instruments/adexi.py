import pandas as pd
import numpy as np
class Adexi:
    def __init__(self,columns,dataframe,jsonData,instrument):
        """
    Parameters
    ----------
    columns: list that contains the names of all the columns,
    dataframe: a pandas dataframe object that contains all the csv file info,
    jsonData: a python dictionary that contains information about each instrument
    
    Attributes
    ----------
    columns: stores the list of columns, used for finding survey question ranges
        type: list
    df: stores the dataframe
        type: datafram
    sections: stores each section from timestamp to complete
        type: list
    nullRow: stores the rows that contain empty values for a section
        type: list
    workingMemory: contains the specific questions for this subscore
        type: list
    inhibition: contains the specific questions for this subscore
        type: list
    total: contains the specific questions for this score
        type: list
    """
        self.instrument = instrument
        self.workingMemory = jsonData[instrument][0][list(jsonData[instrument][0])[0]]
        self.inhibition = jsonData[instrument][0][list(jsonData[instrument][0])[1]]
        self.total = jsonData[instrument][0][list(jsonData[instrument][0])[2]]
        self.columns = columns
        self.df = dataframe
        self.sections = []
        self.jdata = jsonData
        self.nullRow = []

        #name variable for the percetage complete from the json file
        self.percetage_complete_wm = jsonData[instrument][0][list(jsonData[instrument][0])[3]] 
        self.percetage_complete_inh = jsonData[instrument][0][list(jsonData[instrument][0])[4]] 
        self.percetage_complete_total = jsonData[instrument][0][list(jsonData[instrument][0])[5]] 
        
    def getSections(self):
        """
        Loops through each column,
        each time a column name ends with timestamp or complete
        we store the index of that column in the sections list
        """
        for index,column in enumerate(self.columns):
            split = column.split("_")
            if (split[-1] == 'timestamp' or split[-1] == 'complete') and split[0] == 'adexi':
                self.sections.append(index)
    
    def missingData(self, position):
        """
        Selects a starting and ending index from the sections list,
        and looks through each row checking if any there is a missing value.
        If a row has a missing value, we store the index of that row in the nullRow list.
        We do this to ignore this row for calculating the score for this section.
        """
        #start of the section
        start = self.sections[position]+1 
        #end of the section
        end = self.sections[position+1] 
        #selecting all the columns from this section of the dataframe
        selected = self.df.columns[start:end] 
        #for each column
        for i in selected:  
            # we want to know the rows with missing data
            if len(self.df.loc[self.df[i].isnull()].index) > 0: 
                indexes = self.df.loc[self.df[i].isnull()].index
                # we want to know if this row that has missing that is already in the NullRow list
                for x , row in enumerate(indexes):
                    if self.df.loc[self.df[i].isnull()].index[x] not in self.nullRow: 
                        #if is not, we add it to the list
                        self.nullRow.append(row)
                    
    def possibleScoring(self, position, run):
        '''
        Determines if the subscore can be calculated for each user that has missing data
        User indexes with missing values are inside of nullRow,
        Also determines the amount of missing values for each subscore and for the whole survey
        if a subscore or total score cannot be calculated we insert NaN to the column
        
        Parameters
        ----------
        position: int
            which section are we on, this is used to determine the start and ending indexes
            for the current section
        
        run: str
            this is a string holding the run of this section for example 's1_r1_e1', this value
            is used to access the percentageComplete columns for this section
        '''
        #to get the index of the person with missing data
        #because we need the data for the row from only that section and no other
        for x in self.nullRow:
            index = 0
            found = False
            while not found:
                if self.df.index[index] == x:
                    found = True
                else:
                    index+=1
            missingData = pd.to_numeric(self.df.iloc[index,self.sections[position]+1:self.sections[position+1]])
            values = np.isnan(missingData) #returns boolean array

            # identify which columns have data missing
            count = 0
            columnsMissing = []
            while count<len(values):
                if values[count]:
                    columnsMissing.append(count+1)
                count+=1

            count = 0
            wm = True # if true the working memory score can be calculated
            inh = True # if true the inhibition score can be calculated
            amountMissingWM = 0 
            amountMissingINH = 0
            for missing in columnsMissing:
                
                #check if there are values missing for working memory and the amount of values missing
                while count<len(self.workingMemory):
                    if missing == self.workingMemory[count]:
                        wm = False
                        amountMissingWM+=1
                    count+=1
                count = 0
                
                #check if there are values missing for inhibition and the amount missing
                while count<len(self.inhibition):
                    if missing == self.inhibition[count]:
                        amountMissingINH += 1
                        inh = False
                    count+=1
                count = 0
            
            #If wm is false then working memory cannot be calculated so we assign NaN to the WK column
            if wm == False:
                wmColumnIndex = self.df.columns.get_loc(list(self.jdata['adexi'][0])[0]+'_'+ run)
                perCompleteIndexWM = self.df.columns.get_loc(self.instrument+self.percetage_complete_wm+ run)
                self.df.iloc[index,wmColumnIndex]= np.NAN
                #we use the amount of values missing to determine the percentage of values present
                self.df.iloc[index,perCompleteIndexWM] = (9-amountMissingWM)/9*100
                
            #If wm is false then working memory cannot be calculated so we assign NaN to the WK column
            if inh == False:
                inhColumnIndex = self.df.columns.get_loc(list(self.jdata['adexi'][0])[1]+'_'+ run)
                perCompleteIndexINH = self.df.columns.get_loc(self.instrument+self.percetage_complete_inh+ run)
                self.df.iloc[index,inhColumnIndex]= np.NAN
                #we use the amount of values missing to determine the percentage of values present
                self.df.iloc[index,perCompleteIndexINH] = (5-amountMissingINH)/5*100
                
            #If either wm or inh is false then total score cannot be calculated so we assign NaN to the total score column
            if inh == False or wm == False:
                totalscoreColumnIndex = self.df.columns.get_loc(self.total + '_' +run)
                perCompleteIndexTotal = self.df.columns.get_loc(self.instrument+self.percetage_complete_total+ run)
                self.df.iloc[index,totalscoreColumnIndex]= np.NAN
                #we use the amount of values missing to determine the percentage of values present
                self.df.iloc[index,perCompleteIndexTotal] = (14-(amountMissingINH+amountMissingWM))/14*100
                
    
    def addNewColumn(self,score,name,position):
        """
        adds a new column to the dataframe at the specified "position",
        the column data will be the calculated "score"
        and the name will be the "name"
        
        Parameters
        ----------
        score: np.array
            a dataframe column that contains the data to be stored in the new column
        name: str
            the name of the column
        position: int
            the position where the column will be inserted
        """
        self.df.insert(loc = self.sections[position+1]+1,
                  column = name+"_"+self.df.columns[self.sections[position+1]].split("_",1)[1].split("_comp")[0],
                  value=score,
                  allow_duplicates=False) 
    
    def subscore(self, columns_arr,position):
        """
        Calculates the subscore by adding the specified columns,
        it uses the indexes stored in the sections list to go through every section
        for the instrument
        
        Parameters
        ----------
        columns_arr: np.array
            list of the columns to be summed
        position: int
            position in the sections list for this instrument
        """
        selected = self.df.columns[self.sections[position]+1:self.sections[position+1]]
        selectedCols = []
        for i in columns_arr:
            selectedCols.append(selected[i-1])
        return self.df[selectedCols].sum(axis=1)
    
    def percentageComplete(self, name , position):
        '''
        This method creates a column for each subscore and the total scoring and
        gives them a starting value of 100% completion
        This value is then updated in the possibleScoring method according to values missing for the subscores
        
        Parameters
        ----------
        name: str
            string with the name of the column to be added
        position: int
            the position where the column will be inserted
        '''
        run = self.df.columns[self.sections[position+1]].split("_",1)[1].split("_comp")[0]
        location = self.sections[position+1]+1
        column = name + run
        percentage = 100
        
        self.df.insert(loc = location,
                  column = column,
                  value=percentage,
                  allow_duplicates=False) 
    
    def addNewDataColumns(self):
        """
        Adds all the columns for the instrument for each of its sections
        by looping through the sections list
        """
        i = 0
        count = 1
        while i < len(self.sections):
            if i%2 == 0:
                
                #used to determine which rows have missing values
                self.missingData(i)
                
                #calculates the addtion of all the columns
                addition = pd.to_numeric(self.df.iloc[:, self.sections[i]+1:self.sections[i+1]].sum(axis=1))
                #creates the percentage complete columns
                self.percentageComplete(self.instrument+self.percetage_complete_total,i)
                self.percentageComplete(self.instrument+self.percetage_complete_wm,i)
                self.percentageComplete(self.instrument+self.percetage_complete_inh,i)

                
                #columnsArrWM holds the column number to score for the working memory
                columnsArrWM = self.jdata[self.instrument][0][list(self.jdata[self.instrument][0])[0]]
                #columnsArrINH holds the column number to score for the inhibition
                columnsArrINH = self.jdata[self.instrument][0][list(self.jdata[self.instrument][0])[1]]
                #creates the total, inhibition and working memory columns with their calculated values
                self.addNewColumn(addition,self.total, i)
                self.addNewColumn(self.subscore(columnsArrWM,i),list(self.jdata[self.instrument][0])[0], i)
                self.addNewColumn(self.subscore(columnsArrINH,i),list(self.jdata[self.instrument][0])[1], i)
                
                # run holds the session run and event of the current session but splitting the name of _complete
                # and obtaining the 's1_r1_e1' string which we use in the possibleScoring method to add to the name of the new columns
                run = self.df.columns[self.sections[i+1]].split("_",1)[1].split("_comp")[0]
                self.possibleScoring(i,run)
                
                try:
                    #for each section of the adexi we add 6 columns and we need to account for this translation for
                    #the indexing of the next section
                    # 3 columns are from the subscoring and total and 3 are from the percentage complete columns
                    self.nullRow = []
                    self.sections[i+2]+=(6*count) #we update the indexing value from the start of the section(which is the _timestamp index)
                                                  #and
                    self.sections[i+3]+=(6*count) #we update the indexing value from the end of the section (which is the _complete index)
                    #count starts at 0 because at the start we dont need to account for any translation 
                    #since no columns have been inserted
                    #and for every section we increment count since the amount of new columns per section increases by 6
                    #so for the third section count would be 2 giving us a value of 2*6 which is the 12 columns that have been added
                    count+=1
                except IndexError:
                    break;
            i+=1