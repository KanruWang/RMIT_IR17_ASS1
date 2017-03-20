"""
!! Indentation: *1 tab = 4 spaces !!

This is the entry .py file for the indexing module for ASS#1

Importing different modules at the start, using built libraries to read command-line args


"""

# import Python libraries to work with, NO advanced libs, just the ones to make life easier
import sys

# import different modules we wrote
import parseMod
import indexMod

def main(argv):
    sourceFile = ''
    stopList = ''
    printOut = False

    # termList: returned from ParseModule
    termList = []

    # entry point: handle flags and options
    for argvLine in argv:
        if argvLine == '-s':
            # if stop file supplied, it has to be the second arg
            stopList = argv[1]
        else:
            if argvLine == '-p':
                printOut = True
    if len(argv) == 1:
        # sourcefile is always to last one in argv list :)
        sourceFile = argv.pop()
        flagError = False
    sourceFile = argv.pop()
    # get help
    if len(argv) < 1 | len(argv) > 4:
        print 'Invalid arguments:'
        print 'usage: [-s <stoplist>] [-p] <sourcefile>'

    #=================================================// Done with argv
    parseModule = parseMod.ParseModule(sourceFile, stopList)
    termList = parseModule.readDoc()
    # print to stdout if -p supplied
    if printOut == True:
        print termList


if __name__ == "__main__":
    main(sys.argv[1:])