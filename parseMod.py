"""
This is the parse module:

"""
# built in modules
import string

class ParseModule:
    'Parser to handle SGML files'
    def __init__(self, docName, printOut):
        self.docName = docName
        self.docFile = open(docName, "r")
        self.printOut = printOut
        self.docCount = 0
        self.docMap = dict()

    def readDoc(self):
        # start reading the doc
        self.docFile = open(self.docName, "r")
        line = self.docFile.readline()
        # list of term-docID tuple
        termList = []

        #loop through
        # when its not EOF
        while line != '':
            #split into words
            words = line.split(' ') # split on whitespaces
            # reading a new doc
            if words[0].strip() == '<DOC>':
                # read next line and pass to the read new doc func
                line = self.docFile.next()
                self.readDocno(line)
                line = self.docFile.next()
                continue

            # skipping section and length
            if words[0] == '<SECTION>':
                while words[0] != '</SECTION>':
                    line = self.docFile.next()
                    words = line.split(' ')
            if words[0] == '<LENGTH>':
                while words[0] != '</LENGTH>':
                    line = self.docFile.next()
                    words = line.split(' ')

            #strip off the tags and small numbers <= 3 digits
            for word in words:
                # clean up the word first
                cleanWords = self.tokenize(word)
                # normalize the word, and add the returned values
                if cleanWords == None:
                    continue
                # add to the termList
                for cleanWord in cleanWords:
                    termList.append((cleanWord, self.docCount))
            # detect EOF
            try:
                line = self.docFile.next()
            except StopIteration:
                break
        print termList # DEBUG
        print self.docMap

        # close file at the end
        self.docFile.close()
    # =============================// Main function ends //======

    # function that maps ID(docCount) with DOCNO
    def readDocno(self, line):
        # this *line* being passed should contain the docNo
        words = line.split(' ')
        docNo = words[1] # the docNo should always be the 2nd element
        # pair and map id with DOCNO
        self.docMap[str(self.docCount)] = docNo
        # increase the doc count
        self.docCount += 1
        #print 'Doc Count: ' + str(self.docCount) # DEBUG

    # function to tokenize words, remove and clean, return word or None
    # Specs: default length of numbers to be removed is *3*
    # Returns: a array of words, or None
    def tokenize(self, word):
        # strip the word clean
        word = word.strip()
        # return None when the 'word' is NOT a word
        if word.startswith('<') and word.endswith('>'):
            return None
        if word.isdigit() and (len(word) < 3):
            return None

        # start cleaning the word
        word = word.lower()
        # get rid of punctuations except for *hyphen* *single-quote*
        punctuationList = string.punctuation.replace('-', '')
        punctuationList = punctuationList.replace("'", "")
        word = word.translate(None, string.punctuation)

        # break hyphen word into two
        tokens = word.split('-')
        # check for '--' situations
        for token in tokens:
            if token == '':
                tokens.remove(token)
        # check for empty lists
        if len(tokens) == 0:
            return None

        cleanWords = self._normalize(tokens)

        # check and remove empty strings
        for cleanWord in cleanWords:
            if cleanWord == '':
                cleanWords.remove(cleanWord)
        if len(cleanWords) == 0:
            return None
        return cleanWords

    # function to normalize the word, return array of word/s
    # called from within the tokenize func
    def _normalize(self, words):
        cleanWords = []
        for word in words:
            # check for special cases
            if word == "isn't":
                cleanWords.append("is")
                cleanWords.append("not")
                continue

            # assume there's always only one char after the '
            wordList = word.split("'")
            # add the first part of the word in the list
            cleanWords.append(wordList[0])
            if len(cleanWords) == 1:
                continue
            # check for the chars after the '
            if wordList[1] == 'm':
                cleanWords.append("am")
                continue
            if wordList[1] == "re":
                cleanWords.append("are")
                continue
        return cleanWords
    # to output a map
    #def _outputMap(self):
