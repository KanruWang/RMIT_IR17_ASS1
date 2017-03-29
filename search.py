"""
!! Indentation: *1 tab = 4 spaces !!

This is the entry .py file for the search module for ASS#1

Importing different modules at the start, using built libraries to read command-line args


"""

# import Python libraries to work with, NO advanced libs, just the ones to make life easier
import sys
import struct
import parseMod
from util import Lexicon, Termitem, InvertedList

def main(argv):
    lexiFile = ''
    invertList = ''
    mapFile = ''
    queryTerms = []
    # entry point: handle flags and options
    # in case of error:
    if len(argv) < 4:
        print "Argv Error: Not Enough Arguments Passed!"
    for ar in argv:
        if ar == None or ar == '' or ar == ' ':
            print "Argv Error: Null Arguments Passed!"

    # the first 3 args are always: lexicon, invllists, map
    lexiFile = argv[0]
    invFile = argv[1] # Do NOT read all into file at the beginning
    mapFile = argv[2]

    # get all query terms
    rawTerms = argv[3:]
    # tokenize term, using the same function in the parseMod. Returns a list
    queryTerms = processTerms(rawTerms)
    # check for invalid input terms
    if len(queryTerms) == 0:
        print "Your input is INVALID"
        quit()

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

    # I believe this is the end if my code runs well

def processTerms(rawTerms):
    # tokenize term, using the same function in the parseMod
    tokenTerms = []
    for term in rawTerms:
        cleanTerms = parseMod.tokenize(term)
        # check for None
        if cleanTerms == None:
            continue
        else:
            for cleanTerm in cleanTerms:
                tokenTerms.append(cleanTerm)
                # now we have a list of clean term
    return tokenTerms

def readLexicon(lexiFileName):
    lexiFile = open(lexiFileName, 'r')
    lexicon = Lexicon() # construct lexicon Object
    # loop through file when not EOF
    line = lexiFile.readline()
    while line != '':
        line = line.strip()
        termInfo = line.split(' ') # [termStr, freq/BinLength, pointerOffset]
        #print termInfo
        # debug
        if len(termInfo) != 3:
            print "lexicon reading ERROR: TermInfo length NOT 3, should be 3"
        lexicon.addTerm(termInfo[0], termInfo[1], termInfo[2])
        # detect EOF
        try:
            line = lexiFile.next()
        except StopIteration:
            break
    # close file at the end
    lexiFile.close()
    return lexicon

def readMap(mapFileName):
    mapFile = open(mapFileName, 'r')
    mapDict = dict() # key: docID; Value: docName - original
    line = mapFile.readline()
    while line != '':
        mapInfo = line.split(' ')
        # debug
        if len(mapInfo) != 2:
            print "MAP reading ERROR: mapInfo length NOT 3, should be 3"
        mapDict[mapInfo[0]] = mapInfo[1]
        # detect EOF
        try:
            line = mapFile.next()
        except StopIteration:
            break
    #close file at the end
    mapFile.close()
    return mapDict

# read a chunk from binary file, convert and return a invList Object
def readInvList(fileName, offset, length):
    lengthInt = int(length)
    binaryFile = open(fileName, 'rb')
    binaryFile.seek(int(offset), 0) # times 32 to convert it back to bits
    #print offset
    # now we have the pointer moved to the right position
    # raw binary data to unpack two integers for every doc occurrence
    invBinaryList = binaryFile.read(lengthInt*2*4)
    intCount = lengthInt*2
    # create format string based on number of integers
    fmtStr = ""
    for i in range(intCount):
        fmtStr += 'i'
    #print intCount
    #print len(invBinaryList)
    invListTup = struct.unpack(fmtStr, invBinaryList)
    #print invListTup
    # put numbers from tup to list
    invList = []
    for i in range(len(invListTup)):
        invList.append(invListTup[i])
    """
    # read chunk by chunk, solution found on stackoverflow
    n = 32
    # break the full string into 32 bits parts into a list of <docID, docFreq>
    invBinaryList = [invBinaryList[i:i+n] for i in range(0, len(invBinaryList), n)]
    # convert every 32 bits into integer
    invList = []
    for binaryItem in invBinaryList:
        intNumber = int(binaryItem, 2)
        invList.append(intNumber)
    """
    # use iterator to go through this list, put stuff into InvList object
    invListObject = InvertedList()
    it = iter(invList)
    for x in it:
        # directly add into the invlist object docID-docFreq dictionary
        invListObject.setDocFreq(x, next(it))
    binaryFile.close()
    return invListObject


if __name__ == "__main__":
    main(sys.argv[1:])