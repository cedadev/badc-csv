import  badctextfile

import sys

if __name__ == "__main__":
    filename = sys.argv[1]
    fh = open(filename, 'r')
    t = badctextfile.BADCTextFile(fh)
    t.check_complete(1)
    print t
    fh = open('%s.na' % filename,'wb')
    fh.write(t.NASA_Ames())
    fh.close()
