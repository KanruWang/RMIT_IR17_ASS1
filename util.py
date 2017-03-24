"""
utillity module:

contains Object representation of lexicon, term and inverted list
"""

# object models, using chain of responsibility model
class Lexicon:
    #The lexicon object that holds a dictionary of term objects and other functions
    # hash dictionary to store term items
    def __init__(self):
        self.lexiTable = dict()

    # update or add a term item, take term, docID as params
    # Note: the value term mapped to in dictionary is a term object
    def updateTerm(self, term, docID):
        if term in self.lexiTable:
            # if the term key exists, update the term and its invertlist
            self.lexiTable[term].update(docID)
        else:
            # else when the term is new to the dictionary, add it in
            self.lexiTable[term] = Termitem(term, docID)

    # debug function
    def printList(self):
        returnStr = "$ Inverted Index: \n"
        lexiArray = self.lexiTable.items()
        lexiArray.sort(key=lambda tup: tup[0])
        for value in lexiArray:
            key, term = value
            returnStr += term.output() + " \n"
        return returnStr


class Termitem:
    # The item object stored in lexicon, Contains only 3 properties:
    # : term, docFreq, pointer to invertList
    # The initial docID MUST be passed during construction
    def __init__(self, term, docID):
        # properties are made public available
        self.term = term # string value
        self.invertList = InvertedList() # create a new inverted list during construction
        self.docFreq = 0 # initially set to 0 by default, then call update immediately
        # initial update
        self.update(docID)

    # increase the docFreq by 1, and update its posting
    # called when the term is encountered during indexing
    def update(self, docID):
        # increase
        self.docFreq += 1
        # update posting, for the given docID
        self.invertList.update(docID)

    # output function
    def output(self):
        returnStr = "# " + str(self.term) + " ^ " + str(self.docFreq) + " "
        returnStr += self.invertList.outputStr()

        return returnStr

class InvertedList:
    # object representation of the inverted list, each term item has a pointer pointing to this
    def __init__(self):
        # main data structure is a dictionary to store postings
        self.list = dict()
    # Note: the key used in the dictionary is the docID

    # add a new posting or increment the value, which is the in-doc-frequency, depends on if the given key exists
    def update(self, key):
        # check for the existence of the given key
        if key in self.list:
            # if the key / posting is already there:
            # increase the posting's in-doc-frequency by 1
            self.list[key] += 1
        else:
            # if the key / posting is not there yet:
            # create a new posting, set the in-doc-freq to 1
            self.list[key] = 1

    # output function
    def outputStr(self):
        returnStr = " | "
        for key, value in self.list.items():
            returnStr += " <" + str(key) + ", " + str(value) + "> "

        return returnStr