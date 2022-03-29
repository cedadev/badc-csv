import  badctextfile

import sys
from netCDF4 import Dataset


if __name__ == "__main__":
    filename = sys.argv[1]
    fh = open(filename, 'r')
    t = badctextfile.BADCTextFile(fh)
    t.check_complete()
    if filename[-4:] == '.csv':
        filename = filename[:-4]
    fh = open('%s.cdl' % filename,'wb')
    fh.write(t.cdl())
    fh.close()
