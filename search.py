"""
!! Indentation: *1 tab = 4 spaces !!

This is the entry .py file for the search module for ASS#1

Importing different modules at the start, using built libraries to read command-line args


"""

# import Python libraries to work with, NO advanced libs, just the ones to make life easier
import sys
import time
import parseMod
from util import Lexicon, Termitem, InvertedList
from searchMod import SearchModule

def main(argv):
    start_time = time.time()
    # entry point: handle flags and options
    # in case of error:
    if len(argv) < 12:
        print "Argv Error: Not Enough Arguments Passed!"
        print 'Please invoke the program in this format:'
        print '-BM25 -q <query-label> -n <num-results> -l <lexicon> -i <invlists> -m <map>'
        print '            [-s <stoplist>] <queryterm-1> [<queryterm-2> ... <queryterm-N>]'
        quit()

    for ar in argv:
        if ar == None or ar == '' or ar == ' ':
            print "Argv Error: Null Arguments Passed!"
            print 'Please invoke the program in this format:'
            print '-BM25 -q <query-label> -n <num-results> -l <lexicon> -i <invlists> -m <map>'
            print '            [-s <stoplist>] <queryterm-1> [<queryterm-2> ... <queryterm-N>]'
            quit()

    # the files
    queryLabel = argv[2]
    numResults = int(argv[4])
    lexiFile = argv[6]
    invFile = argv[8]
    mapFile = argv[10]
    rawTerms = []
    stopList = None

    # in case of stoplist, get all query terms
    if argv[11] == "-s":
        stopList = argv[12]
        if len(argv) > 12:
            # get all query terms
            rawTerms = argv[13:]
    else:
        # get all query terms.
        rawTerms = argv[11:]

    # have the SearchMod to handle instantiation and query processes
    searchMod = SearchModule(lexiFile, invFile, mapFile, stopList)

    searchMod.startQuery(queryLabel, numResults, rawTerms)

    # =============== / End of Reading Arguments / ===================
    printTime = (time.time() - start_time) * 1000
    print("--- Running time: %s ms ---" % printTime)

    """ =========== / Old codes to refer to / ==============
    # start reading files in
    lexicon = readLexicon(lexiFile)
    mapDict = readMap(mapFile)
    #print mapDict
    # start query: find out which terms got hit first
    termList = []
    for query in queryTerms:
        # when it is in the lexicon dictionary
        if query in lexicon.lexiTable:
            termList.append(lexicon.lexiTable[query])
        else:
            continue
    # now we have a list of TermItem, which got 'hit' by queryTerms; or an empty list
    if len(termList) == 0: # in case of empty list
        print "NONE of your query terms are found in the collection"
        quit()
    # otherwise, start reading the invList based on the info stored in TermItem
    for term in termList:
        #print term.getOffset()
        #print term.getFreq()
        term.setInvList(readInvList(invFile, term.getOffset(), term.getFreq()))
    # now we have a termList with complete term structures: termStr, freq, invList
    # so that we can print now
    for term in termList:
        print term.term
        print str(term.getFreq())
        for docID,docFreq in term.getInvList().list.items():
            invString = mapDict[str(docID)].strip() + ' ' + str(docFreq)
            print invString

    # I believe this is the end if my code runs wel
    """

if __name__ == "__main__":
    main(sys.argv[1:])