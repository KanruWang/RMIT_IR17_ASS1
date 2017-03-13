"""
!! Indentation: *1 tab = 4 spaces !!

This is the entry .py file for the indexing module for ASS#1

Importing different modules at the start, using built libraries to read command-line args


"""

# import Python libraries to work with, NO advanced libs, just the ones to make life easier
import sys, getopt

# import different modules we wrote
import parseMod
import stopMod
import indexMod

def main(argv):
    sourcefile = ''
    stoplist = ''
    output = False
    try:
        opts, args = getopt.getopt(argv,"hsp")
    except getopt.GetoptError:
        print 'usage: index.py [-s <stoplist>] [-p] <sourcefile>'
        sys.exit(2)
    # if no options has been provided
    if len(argv) == 1:
        sourcefile = argv[0]
    print argv

    print 'sourcefile "', sourcefile
    print 'stoplist "', stoplist

if __name__ == "__main__":
    main(sys.argv[1:])