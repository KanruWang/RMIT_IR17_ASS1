"""
!! Indentation: *1 tab = 4 spaces !!

This is the entry .py file for the indexing module for ASS#1

Importing different modules at the start, using built libraries to read command-line args


"""

# import Python libraries to work with, NO advanced libs, just the ones to make life easier
import sys

# import different modules we wrote
import parseMod
import stopMod
import indexMod

def main(argv):
    sourceFile = ''
    stopList = ''
    printOut = False

    # entry point: handle flags and options
    for argvLine in argv:
        if argvLine == '-s':
            # if stop file supplied
            stopList = argv[1]
        else:
            if argvLine == '-p':
                printOut = True
    if len(argv) == 1:
        sourceFile = argv.pop()
        flagError = False
    # get help
    if len(argv) < 1 | len(argv) > 4:
        print 'Invalid arguments:'
        print 'usage: [-s <stoplist>] [-p] <sourcefile>'
    # the sourceFile is always the last one
    sourceFile = argv.pop()

    #=================================================// Done with argv
    parseModule = parseMod.ParseModule(sourceFile, printOut)
    parseModule.readDoc()

if __name__ == "__main__":
    main(sys.argv[1:])