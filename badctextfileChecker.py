import  badctextfile

import sys

if __name__ == "__main__":
    filename = sys.argv[1]
    fh = open(filename, 'r')
    t = badctextfile.BADCTextFile(fh)
    print "Checking basic"
    t.check_complete()
    print "\n\n\nChecking complete"
    t.check_complete(1)
