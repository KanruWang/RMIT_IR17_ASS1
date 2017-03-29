"""
This is the index module:

"""
# just import lexicon class, termItem and InvertedList will be handled in lexicon object and will not be exposed
from util import Lexicon

class IndexModule:
    def __init__(self, termList):
        # the original termlist passed through
        self.termList = termList
        # create an empty lexicon
        self.lexicon = Lexicon()

    # entry function
    def startIndex(self):
        self.sortTermList()
        self.constructIndex()
        self.lexicon.outputIndex()
        #self.printLexicon()

    def sortTermList(self):
        """This function simply sort the term list first"""
        self.termList.sort(key=lambda tup: tup[0])
        return self.termList

    def constructIndex(self):
        """called after the list is sorted"""
        # start reading through the sorted list
        for termTuple in self.termList:
            # extract term and docID
            #print termTuple
            term, docID = termTuple
            self.lexicon.updateTerm(term, docID)
        #self.printLexicon()

    # debug function
    def printLexicon(self):
        result = self.lexicon.printList()
        print result
        with open("testLexi", 'w') as file:
            file.write(result)

