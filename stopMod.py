"""
This is the stop module:
Only have one public function, to process an array of words, remove stop words;
Param: wordList, stopList;
Return: array of cleaned terms, can be empty, empty check dealt upon the chain func;
Data Structure: built in dictionary
"""

class StopModule:
    def __init__(self, stopFileName):
        self.stopFileName = stopFileName
        self.stopList = open(self.stopFileName, "r")
        # map stop list in construction
        self.stopMap = self._constructMap()

    def _constructMap(self):
        self.stopList = open(self.stopFileName, "r")
        stopMap = dict()

        line = self.stopList.readline().strip()  # always strip() to remove '\n'
        # go through the stop list and map them
        while line != '':
            # add to the dictionary
            stopMap[line] = 1
            # detect EOF and move to the next line
            try:
                line = self.stopList.next().strip() # always strip() to remove '\n'
            except StopIteration:
                break
        return stopMap

    # returns a list of cleaned words
    def removeStops(self, wordList):
        cleanWords = []
        # check for null values, return none when detected
        if wordList == None:
            return None
        # start cleaning the wordlist, when key is found in dictionary
        # print self.stopMap
        for word in wordList:
            if self.stopMap.has_key(word) == True:
                #print word
                continue
            else:
                cleanWords.append(word)

            # return None if list is empty
            if len(cleanWords) == 0:
                return None
            return cleanWords