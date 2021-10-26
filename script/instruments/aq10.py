import pandas as pd
import numpy as np
class AQ10:
    '''
    Instance Variables
      ----------
      columns: np.array
          the list of columns in the dataframe 
      dataframe: pandas dataframe
          the dataframe containing all the csv file data
      jsonData: python dictionary
          dictionary containing the keys and values for each instrument
      instrument: str
          name of the instrument
     agree: contains the specific questions for this subscore
        type: list
     disagree: contains the specific questions for this subscore
        type: list
     total: contains the specific questions for this score
        type: list
    '''
    def __init__(self, columns, dataframe, jsonData, instrument):
        
        self.columns = columns
        self.df = dataframe
        self.agree = jsonData[instrument][0][list(jsonData[instrument][0])[0]]
        self.disagree = jsonData[instrument][0][list(jsonData[instrument][0])[1]]
        self.total = jsonData[instrument][0][list(jsonData[instrument][0])[2]]
        self.jdata = jsonData
        self.instrument = instrument
        self.sections = []
        self.score = 0
        self.nullRow = []

        #name variable for the percetage complete from the json file
        self.percetage_complete_agreed = jsonData[instrument][0][list(jsonData[instrument][0])[3]] 
        self.percetage_complete_disagreed = jsonData[instrument][0][list(jsonData[instrument][0])[4]] 
        self.percetage_complete_total = jsonData[instrument][0][list(jsonData[instrument][0])[5]] 
        
    def getSections(self):
        ''' gets all of the sections for this intrument.
            a section is a set of columns ranged from a timestamp column to a complete column
        '''
        for index, column in enumerate(self.columns):
            split = column.split("_")
            if (split[-1] == 'timestamp' or split[-1] == 'complete') and split[0] == 'aq10':
                self.sections.append(index)
                
    def displaySections(self):
        """
        Loops through each column,
        each time a column name ends with timestamp or complete
        we store the index of that column in the sections list
        """
        count = 1
        i = 0
        while i < len(self.sections):
            if i%2==0:
                print(self.df[self.df.columns[self.sections[i]+1:self.sections[i+1]]])
            i+=1
            
        
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
            
    
    def addNewColumn(self,name,position):
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
        # the run for example : s1_e1_r1
        run = self.df.columns[self.sections[position+1]].split("_",1)[1].split("_comp")[0]
        self.df.insert(loc = self.sections[position+1]+1,
                  column = name + "_" + run,
                  value=np.nan,
                  allow_duplicates=False) 
    
    def getScore(self, position,run):
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
            #this holds the questions that if agreed or slightly agreed means we add 1 to the score
            agreedArr = self.jdata[self.instrument][0][list(self.jdata[self.instrument][0])[0]]
            #this holds the questions that if disagreed or slightly disagreed means we add 1 to the score
            disagreedArr = self.jdata[self.instrument][0][list(self.jdata[self.instrument][0])[1]]
            
            #In this loop we go person by person calculating their score and assigning it to the total score column
            count = 0
            people = len(self.df.index)
            empty = False #if true then this row will have an emtpy value and so no total score will be calculated
            while count < people:
                #columns contains all the answers for the person at the count position. when count = 0 
                #we check the answers for the first person and so on
                columns = self.df.iloc[count,self.sections[position]+1:self.sections[position+1]]
                for question in agreedArr:
                    if columns[question-1] == 1 or columns[question-1] == 2:
                        self.score+=1
                    if np.isnan(columns[question-1]) :
                        empty = True
                        break;
                for question in disagreedArr:
                    if columns[question-1] == 3 or columns[question-1] == 4:
                        self.score+=1
                    if np.isnan(columns[question-1]):
                        empty = True
                        break;
                if not empty:
                    scoreColumnIndex = self.df.columns.get_loc(self.total + "_" + run)
                    self.df.iloc[count,scoreColumnIndex]= self.score
                else:
                    scoreColumnIndex = self.df.columns.get_loc(self.total + "_" + run)
                    self.df.iloc[count,scoreColumnIndex]= np.nan
#                 print('this is row ',count,'and it has empty values-',empty) Used this to check out if 
#                 the empty variable was true and the total was nan in the dataframe
                empty = False
                count+=1
                self.score=0
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
            agree = True # if true the working memory score can be calculated
            disagree = True # if true the inhibition score can be calculated
            amountMissingAgree = 0 
            amountMissingDisagree = 0
            for missing in columnsMissing:
                
                #check if there are values missing for working memory and the amount of values missing
                while count<len(self.agree):
                    if missing == self.agree[count]:
                        agree = False
                        amountMissingAgree+=1
                    count+=1
                count = 0
                
                #check if there are values missing for inhibition and the amount missing
                while count<len(self.disagree):
                    if missing == self.disagree[count]:
                        amountMissingDisagree += 1
                        disagree = False
                    count+=1
                count = 0
            
            #If wm is false then working memory cannot be calculated so we assign NaN to the WK column
            if agree == False:
                perCompleteIndexAgree = self.df.columns.get_loc(self.instrument+self.percetage_complete_agreed+ run)
                #we use the amount of values missing to determine the percentage of values present
                self.df.iloc[index,perCompleteIndexAgree] = (4-amountMissingAgree)/4*100
                
            #If wm is false then working memory cannot be calculated so we assign NaN to the WK column
            if disagree == False:
                perCompleteIndexDisagree = self.df.columns.get_loc(self.instrument+self.percetage_complete_disagreed+ run)
                #we use the amount of values missing to determine the percentage of values present
                self.df.iloc[index,perCompleteIndexDisagree] = (6-amountMissingDisagree)/6*100
                
            #If either wm or inh is false then total score cannot be calculated so we assign NaN to the total score column
            perCompleteIndexTotal = self.df.columns.get_loc(self.instrument+self.percetage_complete_total+ run)
            #we use the amount of values missing to determine the percentage of values present
            self.df.iloc[index,perCompleteIndexTotal] = (10-(amountMissingDisagree+amountMissingAgree))/10*100
                
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
        i = 0
        count = 1
        while i < len(self.sections):
            if i%2 == 0:
                '''need to drop cells and store them in a new variable
                and only add the scores to the rows without missing data
                '''
                self.missingData(i)
                #creates the percentage complete columns
                self.percentageComplete(self.instrument+self.percetage_complete_total,i)
                self.percentageComplete(self.instrument+self.percetage_complete_agreed,i)
                self.percentageComplete(self.instrument+self.percetage_complete_disagreed,i)
                
                self.addNewColumn(self.total, i)
                run = self.df.columns[self.sections[i+1]].split("_",1)[1].split("_comp")[0]
                self.getScore(i,run)
                self.possibleScoring(i,run)
                try:
                    self.nullRow = []
                    #for each section of the adexi we add 1 column and we need to account for this translation for
                    #the indexing of the next section
                    # its only the total score column
                    self.sections[i+2]+=(4*count) #we update the indexing value from the start of the section(which is the _timestamp index)
                                                  #and
                    self.sections[i+3]+=(4*count) #we update the indexing value from the end of the section (which is the _complete index)
                    #count starts at 0 because at the start we dont need to account for any translation 
                    #since no columns have been inserted
                    #and for every section we increment count since the amount of new columns per section increases by 1
                    #so for the third section count would be 2 giving us a value of 2*1 which is the 2 columns that have been added
                    count+=1
                except IndexError:
                    break;
            i+=1