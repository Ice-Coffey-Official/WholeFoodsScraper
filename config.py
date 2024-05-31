import random

class config:
     
    def __init__(self):
        self.__states__ = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
        self.__defaultBackoff__ = 3 #may not work with values under 3. This is the minimum number of seconds the program waits between clicks on webpages.
        self.__variableBackoff__ = 2 #how random the interval between web page clicks are. "0" means it clicks every $defaultBackoff (default 3) seconds. "2" means it clicks between $defaultBackoff (default 3) seconds and $defaultBackoff (default 5) seconds.
        self.__pathSaveName__ = "data" #The Save Path Name
        self.__saveAs__ = ['csv', 'excel']

    def getStates(self):
        return self.__states__
    
    def getBackoff(self):
        return self.__defaultBackoff__

    def getVariableBackoff(self):
        return random.random()*self.__variableBackoff__
    
    def getSavePath(self):
        return self.__pathSaveName__
    
    def getSaveAs(self):
        return self.__saveAs__