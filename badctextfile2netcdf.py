#!/usr/bin/env python

"""
badctextfile2netcdf.py
======================
Tool to create CF 1.7 conformant netCDF files
from supplied BADC-CSV formatted file


Written by: G A Parton

Creation: 26th February 2016

Version 1.0: initial scripting
Version 1.1: moving netCDF specialisation code into this module

still to do:
1) mapping between badc-csv version 1 attributes and CF equivalent
2) checks for CF-1.7 conformance and error message flagging


"""



import  badctextfile

import sys
from netCDF4 import Dataset
from netCDF4 import Dataset
import numpy as np


class BADCTextFile(badctextfile.BADCTextFile):
    """
    specialisation of the BADCTextFile class to add in components to create netCDF files from 
    submitted badc-csv formatted file
    """
    
    
    
     = {'creator': ['creator_name','institution']
                         ,'':[]
                         }
    
    header_name_mapper = [("Conventions",          ) # change to CF if all OK
                         ,("long_name",             (['long_name','units'], longNameSplit)) # split to get units
                         ,("coordinate_variable",   (['axis'],checkValidAxis)) # only 4 permitted in CF
                         ,("creator",               (['creator_name','institution'],))
                         ,("source",                (['source'],))
                         ,("observation_station",   (['platform_name'],))
                         ,("activity",              (['project'],))
                         ,("feature_type",          (['feature_type'],checkFeatureType))
                       #  ,("location",  ['platform_location']           ) # actually bad-csv isn't defined the same!!
                         ,("date_valid",            ([date_valid],))
                         ,("last_revised_date",     (['last_revised_date'],sortDate))
                         ,("history",               (['history'], joinLines))  ### note - want to check the time stamp too?
                         ,("standard_name",         (['standard_name','units','CF'],standardNameSplit)) # how will this cope with units being defied in two places?
                         ,("title",                 (['title'],))
                         ,("comments",              (['comment'],joinLines))
                         ,("contributor",           ([],))
                         ,("height",                ([],))
                         ,("reference",             ([],))
                         ,("rights",                (['licence'],joinLines))
                         ,("valid_min",             ([],))
                         ,("valid_max",             ([],))
                         ,("valid_range",           ([],))
                         ,("type",                  (['type'],checkPermittedTypes))
                         ,("cell_method",           (['cell_methods'],)) # need to update badc-csv to get name correct!             
                         ,("add_offset",            ([],))
                         ,("scale_factor",          ([],))
                         ,("flag_values",           (['flag_values'],joinString))
                         ,("flag_meanings",         (['flag_meanings'],joinString))
                         ]

    def checkPermittedTypes(self,type_to_check):
        
        verdict = 0
                
        if ininstance(type_to_check, char):
            verdict = 1
        elif  ininstance(type_to_check, byte):
            verdict = 1
        elif  ininstance(type_to_check, short):
            verdict = 1
        elif  ininstance(type_to_check, int):
            verdict = 1
        elif  ininstance(type_to_check, float):
            verdict = 1
        elif  ininstance(type_to_check, real):
            verdict = 1
        elif  ininstance(type_to_check, double):
            verdict = 1
    
        return verdict
    
    def longNameSplit(self,long_name)
        
        return
        
    def standardNameSplit(self,standard_name)
    
        return
    
    def sortDate(self,date_in):
        """
        function to sort out the date from badc-csv to match that required for 
        it to be the correct iso type

        """
        
        date_out = date_in
        
        
        return date_out

    
    def joinLines(self,existing_line,new_line):
        """
        joins lines into one string for netCDF file
        """
        
        full_line = '\n '.join(existing_line,new_line)
        
        return full_line
    
    def checkFeatureType(self,feature_type):
        """
        Function to check that the feature_type given is a valid one
        from the CF list
        """
        verdict = 0
        
        permitted_types = [ 'point'
                          , 'timeSeries'
                          , 'trajectory'
                          , 'profile'
                          , 'timeSeriesProfile'
                          , 'trajectoryProfile'
                          ]
                          
        if feature_type in permitted_types:
            verdict = 1
    
        return verdict
    def checkValidAxis(self,coordinate):
        
        """
        function to check that the coordinate variable given is a permitted CF variable or not
        
        T,X,Y,Z permitted
        
        """
        
        verdict = 0
        
        if coordinate in ['T','X','Y','Z']:
            verdict =1
               
        return verdict
    
    
    
    def make_netcdf(self, badc_csv_filename):

        """
        This is the actual code to construct the netCDF file - 
        hopefully a CF compiant one
        
        First it handles the global attributes, then the variables 
        and finally adds the data.
        
        """
    
        dataset = Dataset(badc_csv_filename, 'w', format='NETCDF4')

        # set global attributes

        self._metadata.nc(dataset)


        # set variable attributes and add data for each variable
        for col_ind, col_ref in enumerate(self.colnames()):
            
           
            try:
                col_name = 'var%s'% int(col_ref)
            except:
                col_name = col_ref

            var_type = self._metadata.varRecords[col_ref]['type'][0].strip()

            values = np.asarray(self[col_ind])
            

            #add the data for the variable
            dataset.variables[col_name][:] = values



        dataset.close()
        
class BADCTextFileMetadata(badctextfile.BADCTextFileMetadata):    

    """
    Specialisation of the BADCTextFileMetadata class to add in
    components needed to create CF-compliant netCDF files from 
    badc-csv formatted files.
    
    This will not fully respect the entire ordering of metadata 
    give, but will group all global attributes together and 
    all attributes of each variable together. The order of appearance
    of these items will be respected though. Where multiple 
    attribute lines are given in badc-csv file (e.g. comment lines
    are spread over more than one line for ease of reading) these
    are appended together for the netCDF file. In these cases they 
    are joined by a ', ' except for comment lines where line breaks ('\n') 
    are added.
    
    Finally, where the badc-csv metadata field exists in the badc-csv standard
    and doesn't match the name of the equivalent CF attribute field
    then these are mapped over, unless explicitily stated in the badc-csv file 
    as well.
    
    """

    def nc(self, ncfile_obj):
        
        # set this flag assuming that there are no issues
        # we can still produce a netCDF file, but it may not 
        # be CF compliant
        
        passes_cf_conformance = 1
        
        
        for label, values in self.globalRecords:
            print label, values
            
            if label == 'Conventions':
                pass
            
            elif label in ncfile_obj.ncattrs():
                print values
                values = ncfile_obj.getncattr(label) + '\n ' + ', '.join(values)
                ncfile_obj.setncattr(label,values)    
            else:
                values = ', '.join(values)
                ncfile_obj.setncattr(label, values)        
        
        if ncfile_obj.history:
                     
            ncfile_obj.history = ncfile_obj.history + '\n File created from original BADC-CSV formatted file'
        
        print self.globalRecords
        




        # set up dimensions
        # there's just the one dimension here - as all BADC, CSV data are just one-dimensional anyway...
        # so make use of a generic "dim"

        ncfile_obj.createDimension('dim', None)
        
        # set variable attributes
        
        variables_dict = {}
                
        # first look for specific variable attributes and set these
        # then cope with anything else that remains
        # first set up all the variables based on the keys of the variable dictionary:
            
        for col_ref in self.varRecords.keys():
            
            try:
                col_name = 'var%s'% int(col_ref)
            except:
                col_name = col_ref
            
            var_type = self.varRecords[col_ref]['type'][0].strip()
            variable_to_add = ncfile_obj.createVariable(col_name,var_type,('dim',))
    
            # now to set variable attributes:
        
            for label, values in self.varRecords[col_ref].items():
                # in some cases we'll need to handle things in a special way...
                if label == 'long_name':
                    variable_to_add.setncattr(label, values[0])
                    variable_to_add.setncattr('units', values[1])
                
                elif label == 'standard_name':
                    variable_to_add.setncattr(label, ', '.join(values[0:1]))
                    
                elif label == 'type':
                    continue
                
                elif label == 'comment':
                
                    value_string = string.join(values, '\n ')
                    variable_to_add.setncattr(label, value_string)
            
                # just need to add in other translations from badc-csv to cf names in here...
                
                                
                else:

                    value_string = string.join(values, ', ')
                    variable_to_add.setncattr(label, value_string)


        #finally, if no conformance issues, then we can set the CF conventions line:
        
        if passes_cf_conformance:
            ncfile_obj.Conventions = 'CF 1.6'


if __name__ == "__main__":
    filename = sys.argv[1]
    fh = open(filename, 'r')
    t = BADCTextFile(fh)
    t.check_complete()
    if filename[-4:] == '.csv':
        filename = filename[:-4]
    t.make_netcdf('%s.nc' % filename)
