"""
utillity module:

contains Object representation of lexicon, term and inverted list
"""

# object models, using chain of responsibility model
class Lexicon:
    #The lexicon object that holds a dictionary of term objects and other functions
    # hash dictionary to store term items
    def __init__(self):
        # this will store a dictionary of TermItem objs, dict -> <termStr, TermItemObject>
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

    def addTerm(self, term, freq=None, offset=None):
        self.lexiTable[term] = Termitem(term)
        if freq != None:
            self.lexiTable[term].setFreq(freq)
        else:
            print "Adding term with NO frequency"
        if offset != None:
            self.lexiTable[term].addOffset(offset)
        else:
            print "Adding term with NO offset pointer"

    # debug function
    def printList(self):
        returnStr = "$ Inverted Index: \n"
        lexiArray = self.lexiTable.items()
        lexiArray.sort(key=lambda tup: tup[0])
        for value in lexiArray:
            key, term = value
            returnStr += term.printItem() + " \n"
        return returnStr

    # output lexicon in lexicon file
    # assume sorted array being passed
    def outputIndex(self):
        lexiFile = open("lexicon", 'w')
        invFile = open("invlists", 'wb')
        lexiArray = self.lexiTable.items()
        lexiArray.sort(key=lambda tup: tup[0])
        # loop through the list
        pointerCount = 0
        for key, termItem in lexiArray:
            # get to the inverted list now
            invStr = termItem.invertList.outputBinary()
            invFile.write(invStr)
            # construct a proper pointer
            # eg. 'termString' 2 100  ==> can later on be split when reading from file
            lexiStr = termItem.term + ' ' + str(termItem.docFreq) + ' ' + str(pointerCount) + '\n'
            lexiFile.write(lexiStr)
            # length of 1 integer is always 32 bis
            # pointerOffset = lengthOfListString / 32
            pointerCount += (len(invStr)/32)
        # close file
        lexiFile.close()
        invFile.close()

class Termitem:
    # The item object stored in lexicon, Contains only 3 properties:
    # : term, docFreq, pointer to invertList
    # The initial docID MUST be passed during construction
    def __init__(self, term, docID=None):
        # properties are made public available
        self.term = term # string value
        self.invertList = InvertedList() # create a new inverted list during construction
        self.docFreq = 0 # initially set to 0 by default, then call update immediately
        # initial update ONLY when docID is provided
        if docID != None:
            self.update(docID)

    # increase the docFreq by 1, and update its posting
    # called when the term is encountered during indexing
    def update(self, docID):
        # increase
        self.docFreq += 1
        # update posting, for the given docID
        self.invertList.update(docID)

    def addOffset(self, offset):
        self.offset = offset
    def getOffset(self):
        #debug
        if self.offset == None:
            print "Offset pointer NOT set"
            return None
        else:
            return self.offset

    def setFreq(self, freq):
        self.docFreq = freq

    def getFreq(self):
        return self.docFreq

    def setInvList(self, invList):
        self.invertList = invList

    def getInvList(self):
        return self.invertList

    # output function
    def printItem(self):
        returnStr = "# " + str(self.term) + " ^ " + str(self.docFreq) + " "
        returnStr += self.invertList.outputStr()

        return returnStr


class InvertedList:
    # object representation of the inverted list, each term item has a pointer pointing to this
    def __init__(self):
        # main data structure is a dictionary to store postings
        self.list = dict() # (docID : docFreq)
    # Note: the key used in the dictionary is the docID; value is docFreq

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

    def setDocFreq(self, key, value):
        self.list[key] = value

    # output function
    def outputStr(self):
        returnStr = " | "
        for key, value in self.list.items():
            returnStr += " <" + str(key) + ", " + str(value) + "> "

        return returnStr

    # output all the entire list in binary numbers
    def outputBinary(self):
        binaryStr = ""
        listArray = self.list.items()
        for docID, docFreq in listArray:
            binaryStr += self.toBinary(docID)+self.toBinary(docFreq)
        return binaryStr

    # returns binary string of the passed integer in 32 bits
    def toBinary(self, number):
        return format(int(number), '032b')
