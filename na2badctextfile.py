#


import badctextfile
import re
import string

unitre = re.compile(r'(.*) *\((.*)\)$')


def parse_NASA_Ames_1001(fh, fhw):

        f = badctextfile.BADCTextFile(fhw)
    
        #  a NASA-Ames file 1001 FFI
        line = fh.readline()
        bits = line.split()
        NHLINES, FFI = bits[0:2]
        NHLINES = int(NHLINES)
        FFI = int(FFI)
        if FFI != 1001: raise Exception("Not right FFI. only 1001")

        # add creator
        creator = fh.readline().strip()
        inst = fh.readline().strip()
        creator = (creator, inst)
        f.add_metadata('creator',creator)

        # add source (DPT)
        source = fh.readline().strip()
        f.add_metadata('source',source)
           
        # add activiey
        activity = fh.readline().strip()
        f.add_metadata('activity',activity)
    
        # disk 1 of 1
        diskset = fh.readline().strip()
        f.add_metadata('diskset', diskset)
        
        # dates
        dates = fh.readline().strip()
        bits = dates.split()
        bits = map(int, bits)
        date_valid = "%2.2d-%2.2d-%2.2d" % (bits[0], bits[1], bits[2])
        last_revised_date = "%2.2d-%2.2d-%2.2d" % (bits[3], bits[4], bits[5])
        f.add_metadata('date_valid',date_valid)
        f.add_metadata('last_revised_date',last_revised_date)  
    
        # ??
        xx = fh.readline().strip()
        f.add_metadata('xx', xx)
    
        # coord variable
        coord = fh.readline().strip()
        mo = unitre.match(coord)
        if mo: long_name = (mo.group(1), mo.group(2))
        else: long_name = (coord, '?')
        f.add_metadata('coordinate_variables', 0)
        f.add_metadata('long_name', long_name, 0)
            
        # number of variables not coord variable
        nvar = fh.readline().strip()
        nvar = int(nvar)
    
        #scale factors
        sf = fh.readline().strip()
        sf = sf.split()
        for i in range(nvar):
            if float(sf[i]) != 1.0:
                f.add_metadata('scale_factor',float(sf[i]),i+1)

        # valid max
        vm = fh.readline().strip()
        vm = vm.split()
        for i in range(nvar):
            f.add_metadata('valid_max',float(vm[i]),i+1)
                    
        # variable names
        for i in range(nvar):
            var = fh.readline().strip()
            mo = unitre.match(var)
            if mo: long_name = (mo.group(1), mo.group(2))
            else: long_name = (var, '?')
            f.add_metadata('long_name', long_name, i+1)

        # normal comments
        nncoms = fh.readline().strip()
        nncoms = int(nncoms)
        ncoms = ''
        for i in range(nncoms):
            line = fh.readline()
            ncoms = ncoms+ line
        f.add_metadata('NASA-Ames Nornal comments',ncoms.strip())    

        # spacial comments
        nscoms = fh.readline().strip()
        nscoms = int(nscoms)
        scoms = ''
        for i in range(nscoms):
            line = fh.readline()
            scoms = scoms+ line
        f.add_metadata('NASA-Ames Special comments',scoms.strip())    

        # data space seperated
        while 1:
            dataline = fh.readline()
            if dataline == '': break
            dataline = dataline.strip()
            datavalues = dataline.split()
            f.add_datarecord(datavalues)
                    
    
        return f
    

if __name__ == "__main__":


    fhw = open(r'he970405.hc2.csv','w')
    fh  = open(r'he970405.hc2',)
    f = parse_NASA_Ames_1001(fh, fhw)
    fhw.write("%s" %f)
    fhw.close()
    print f

