"""
This is the Search Module, separated out from the search entry file,
to follow a better practice and improvement on management

"""
# Import dependencies
import sys
import heapq
import struct

import parseMod
from util import Lexicon, Termitem, InvertedList
from stopMod import StopModule
from expansionMod import ExpansionModule
from BM25Mod import BM25

class SearchModule:
    def __init__(self, lexiFile, invFile, mapFile, stopList):
        # start initialization:
        self.totalDoc = 0
        # start read the files in
        self.lexicon = self.readLexicon(lexiFile)
        self.weightDict = dict()
        self.mapDict = self.readMap(mapFile)
        self.lenDict = self.readLengthMap()
        self.avgLength = self.avgDocLength()
        self.invFile = invFile
        # ========== / Setup is Done / ===========
        self.bm25 = BM25(self.totalDoc, self.avgLength)
        # self.rankedHeap = []

    def startQuery(self, queryTerms):
        # Now we have a clean nice list of query terms to start with
        # Start following the Query Processing Algo
        HTable = dict()
        for termKey in queryTerms:
            # check if term is recorded
            if termKey not in self.lexicon.lexiTable:
                continue

            # Terms are wrapped in TermItem Object
            term = self.lexicon.getTerm(termKey)
            # Fetch the invList, then the term item obj has its invList
            term.setInvList(self.readInvList(self.invFile, term.getOffset(), term.getFreq()))
            invList = term.getInvList()
            # through all the (docID, Term-in-Doc_Freq)
            for id, f_dt in invList.toIterative():
                # calculate BM25
                # 2 cases, original query or expanded query,
                # original query with term.weight = 0
                if term.weight == 0:
                    score = self.bm25.getSimScore(term.getInvList().list[id], term.getFreq(), self.lenDict[id])
                else:
                    score = self.bm25.getWeightedScore(term.weight, term.getInvList().list[id], self.lenDict[id])
                # print score
                if id in HTable:
                    HTable[id] += score
                else:
                    HTable[id] = score
        # if no term being hit
        if len(HTable) == 0:
            print "None of your query is in the documents!"
            quit()

        # all terms and their docs are processed
        # use Doc Weight, and put HTable into a Heap
        rankHeap = []
        for docID, accumulator in HTable.iteritems():
            HTable[docID] = accumulator / float(self.weightDict[str(docID)])
            # present Result, using a MAX HEAP
            # because heap in python always pops the smallest value, so we invert the value of key
            heapq.heappush(rankHeap, (HTable[docID], docID))

        # once we have done the search and all the hard work, return the ranked Heap
        return list(rankHeap)

    def presentResult(self, queryLabel, numResults, rankHeap):
        for i in range(numResults):
            try:
                invScore, docID = heapq.heappop(rankHeap)
                # print docID, invScore
                score = invScore * -1
                print queryLabel, self.mapDict[str(docID)], str(i + 1), str(score)
            except IndexError:
                break

    # ======== / Reading & Setup Functions / =========

    def processTerms(self, rawTerms):
        # in case of empty rawTerms list:
        if len(rawTerms) == 0:
            return []

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
        return list(tokenTerms)

    def readLexicon(self, lexiFileName):
        lexiFile = open(lexiFileName, 'r')
        lexicon = Lexicon()  # construct lexicon Object
        # loop through file when not EOF
        line = lexiFile.readline()
        while line != '':
            line = line.strip()
            termInfo = line.split(' ')  # [termStr, freq/BinLength, pointerOffset]
            # print termInfo
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

    def readMap(self, mapFileName):
        mapFile = open(mapFileName, 'r')
        mapDict = dict()  # key: docID; Value: docName - original
        line = mapFile.readline()
        while line != '':
            mapInfo = line.split(' ')
            # debug
            # if len(mapInfo) != 2:
            #    print "MAP reading ERROR: mapInfo length NOT 3, should be 3"
            mapDict[mapInfo[0]] = mapInfo[1]

            # modified to count total number of docs
            self.totalDoc += 1
            # print mapInfo[2]
            self.weightDict[mapInfo[0]] = mapInfo[2]

            # detect EOF
            try:
                line = mapFile.next()
            except StopIteration:
                break
        # close file at the end
        mapFile.close()
        return mapDict

    # read a chunk from binary file, convert and return a invList Object
    def readInvList(self, fileName, offset, length):
        lengthInt = int(length)
        binaryFile = open(fileName, 'rb')
        binaryFile.seek(int(offset), 0)  # times 32 to convert it back to bits
        # print offset
        # now we have the pointer moved to the right position
        # raw binary data to unpack two integers for every doc occurrence
        invBinaryList = binaryFile.read(lengthInt * 2 * 4)
        intCount = lengthInt * 2
        # create format string based on number of integers
        fmtStr = ""
        for i in range(intCount):
            fmtStr += 'i'
        # print intCount
        # print len(invBinaryList)
        invListTup = struct.unpack(fmtStr, invBinaryList)
        # print invListTup
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

    def readLengthMap(self):
        lengthMapFile = open("lenMap", "r")
        lenDict = dict()
        line = lengthMapFile.readline()

        while line != '':
            mapInfo = line.split(' ')
            lenDict[int(mapInfo[0])] = mapInfo[1].strip('\n')

            # detect EOF
            try:
                line = lengthMapFile.next()
            except StopIteration:
                break
        return lenDict

    def avgDocLength(self):
        sumLength = 0
        for id,length in self.lenDict.iteritems():
            sumLength += int(length)
        avgLength = sumLength / len(self.lenDict)
        return avgLength
