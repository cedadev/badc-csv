import pytest

from badc_csv.badctextfile import BADCTextFile, BADCTextFileMetadataIncomplete


# what is the difference between badctextfile and badctextfilewarn
def test_BADCTextFile_basic():
    fh = open('./tests/simple-example.csv', 'r')
    f = BADCTextFile(fh)
    f.check_valid()

    f.check_colrefs()

    # check basic compliance
    f.check_complete(level='basic')

    # check complete compliance - should fail
    with pytest.raises(BADCTextFileMetadataIncomplete) as exc:
        f.check_complete(level='complete')
    
    assert str(exc.value) == str(['Global metadata missing: source, required for complete compliance', 
                              'Global metadata missing: observation_station, required for complete compliance', 
                              'Global metadata missing: activity, required for complete compliance', 
                              'Global metadata missing: feature_type, required for complete compliance', 
                              'Global metadata missing: location, required for complete compliance', 
                              'Global metadata missing: date_valid, required for complete compliance', 
                              'Global metadata missing: last_revised_date, required for complete compliance', 
                              'Global metadata missing: history, required for complete compliance', 
                              'Column metadata missing: type missing for 1, required for complete compliance', 
                              'Column metadata missing: type missing for 2, required for complete compliance', 
                              'Column metadata missing: type missing for 3, required for complete compliance'])



    assert f.colnames() == ('1', '2', '3')

    assert f.nvar() == 3

    assert len(f) == 5

    # test get data
    # should they be strings?
    assert f[0] == ['0.8', '1.1', '2.4', '3.7', '4.9']
    assert f[1] == ['2.4', '3.4', '3.5', '6.7', '5.7']
    assert f[2] == ['2.3', '3.3', '3.3', '6.4', '5.8']

    # test get metadata
    # tuple in a list?
    assert f['location_name'][0][0] == 'Rutherford Appleton Lab'

    # test get variable metadata
    assert f._metadata.varRecords['2']['long_name'][0] == 'air temperature'
    assert f._metadata.varRecords['2']['long_name'][1] == 'K'

    # test adding a variable
    # should these be strings?
    d2 = ('2.2', '4.4', '5.7', '15.2', '16.8')
    f.add_variable('4',d2)
    assert f[3] == ['2.2', '4.4', '5.7', '15.2', '16.8']

    # test adding metadata
    f.add_metadata(label='long_name', values=('height', 'm'), ref='4')
    for k,v in f._metadata.varRecords['4'].items():
        assert k == 'long_name'
        assert v == ['height', 'm']
    
    # test adding data record
    f.add_datarecord(['5.2','3.4','6.7','18.2']) # should i add as string or not??
    assert f[0] == ['0.8', '1.1', '2.4', '3.7', '4.9', '5.2']
    assert f[1] == ['2.4', '3.4', '3.5', '6.7', '5.7', '3.4']
    assert f[2] == ['2.3', '3.3', '3.3', '6.4', '5.8', '6.7']
    assert f[3] == ['2.2', '4.4', '5.7', '15.2', '16.8', '18.2']

    # test add metadata
    f.add_metadata('history', 'Testing out badc-csv code on this file', 'G')
    assert f._metadata.globalRecords[-1][0] == 'history'
    assert f._metadata.globalRecords[-1][1] == ('Testing out badc-csv code on this file',)

     # check that file is still valid and basic level compliant
    f.check_valid()

    f.check_colrefs()

    # check basic compliance
    f.check_complete(level='basic')

    # should this be called csv?
    assert f.cvs() == repr(f) == 'Conventions,G,BADC-CSV,1\ntitle,G,My data file\ncreator,G,Prof W E Ather,Reading\ncontributor,G,Sam Pepler,BADC\ncreator,G,A. Pdra\nlocation_name,G,Rutherford Appleton Lab\nhistory,G,Testing out badc-csv code on this file\nlong_name,1,time,days since 2007-03-14\ncoordinate_variable,1,x\nlong_name,2,air temperature,K\nlong_name,3,met station air temperature,K\ncreator,3,unknown,Met Office\nlong_name,4,height,m\nData\n1,2,3,4\n0.8,2.4,2.3,2.2\n1.1,3.4,3.3,4.4\n2.4,3.5,3.3,5.7\n3.7,6.7,6.4,15.2\n4.9,5.7,5.8,16.8\n5.2,3.4,6.7,18.2\nEnd Data\n'

    # test cdl
    assert f.cdl() == '''// This CDL file was generated from a BADC text file file
netcdf foo { 
dimensions:
   point = 6;

variables: 
    var1 (point);
    var2 (point);
    var3 (point);
    var4 (point);

// variable attributes
        varcoordinate_variable:1 = "x";
        varlong_name:2 = "air temperature, K";
        varcreator:3 = "unknown, Met Office";
        varlong_name:4 = "height, m";
// global attributes
        :Conventions = "BADC-CSV, 1";
        :title = "My data file";
        :creator = "Prof W E Ather, Reading";
        :contributor = "Sam Pepler, BADC";
        :creator1 = "A. Pdra";
        :location_name = "Rutherford Appleton Lab";
        :history = "Testing out badc-csv code on this file";

data:
var1 = 0.8, 1.1, 2.4, 3.7, 4.9, 5.2;
var2 = 2.4, 3.4, 3.5, 6.7, 5.7, 3.4;
var3 = 2.3, 3.3, 3.3, 6.4, 5.8, 6.7;
var4 = 2.2, 4.4, 5.7, 15.2, 16.8, 18.2;
}
'''

    # test NASA Ames format
    assert f.NASA_Ames() == '''39 1001
Prof W E Ather; A. Pdra
Reading


1 1
None    None
0.0
time (days since 2007-03-14)
3








time (days since 2007-03-14)
air temperature (K)
met station air temperature (K)
height (m)
1
File created from BADC text file
15
BADC-CSV style metadata:
Conventions,G,BADC-CSV,1\r
title,G,My data file\r
creator,G,Prof W E Ather,Reading\r
contributor,G,Sam Pepler,BADC\r
creator,G,A. Pdra\r
location_name,G,Rutherford Appleton Lab\r
history,G,Testing out badc-csv code on this file\r
long_name,1,time,days since 2007-03-14\r
coordinate_variable,1,x\r
long_name,2,air temperature,K\r
long_name,3,met station air temperature,K\r
creator,3,unknown,Met Office\r
long_name,4,height,m\r
0.8 2.4 2.3 2.2
1.1 3.4 3.3 4.4
2.4 3.5 3.3 5.7
3.7 6.7 6.4 15.2
4.9 5.7 5.8 16.8
5.2 3.4 6.7 18.2
'''


def test_BADCTextFile_complete():
    fh = open('./tests/badc-csv-full-example1.csv', 'r')
    f = BADCTextFile(fh)
    f.check_valid()

    f.check_colrefs()

    # check basic compliance
    f.check_complete(level='basic')

    # check complete compliance
    f.check_complete(level='complete')
    
    assert f.colnames() == tuple([str(i) for i in range(1,36)])

    assert f.nvar() == 35

    assert len(f) == 8

    # test get data
    # should they be strings?
    assert f[0] == ['2009','2009', '2009', '2009', '2009', '2009', '2009', '2009']
    assert f[-1] == ['-9999999','-9999999', '-9999999', '-9999999', '-9999999', '-9999999', '-9999999', '-9999999']

    # test get global metadata
    # tuple in a list?
    assert f['creator'][0][0] == 'G A Parton'
    assert f['creator'][0][1] == 'British Atmospheric Data Centre'

    # test get variable metadata
    f._metadata.varRecords['20']['long_name'][0] == 'Type of aircraft data relay system'
    f._metadata.varRecords['20']['long_name'][1] == '1'

    # test adding a variable
    # should these be strings?
    d2 = ('0')*8
    f.add_variable('36',d2)
    assert f[-1] == ['0']*8
    # have to add long name and type for this variable to make sure it is still compliant
    f.add_metadata(label='long_name', values=('test', 'm'), ref='36')
    f.add_metadata(label='type', values=('float'), ref='36')

    # test add variable metadata
    f.add_metadata(label='scale_factor', values=('test'), ref='9')

    n = 0
    for k,v in f._metadata.varRecords['9'].items():
        if k == 'scale_factor':
            assert v == ['test']
            n += 1
    if n < 1:
        raise Exception 
    
    # test adding data record
    f.add_datarecord(['2009','5','6','12','0','-9999999','2009','5','6','12','4','AIRCRAFT','TEST','44.4','11.02','1500','-9999999','-9999999','0','3','-9999999','-9999999','6','-9999999','293','2.1','-9999999','-9999999','-9999999','-9999999','279.7','-9999999','-9999999','0','-9999999', '0']) # should i add as string or not??
    assert f[12] == ['EU6349', 'EU6349', 'CNJCA314', 'CNJCA317', 'JP9Z58UZ', 'JP9Z5Y6Z', 'EU0583', 'EU0362', 'TEST']

#     # test add metadata
    f.add_metadata('history', 'Testing out badc-csv code on this file', 'G')
    assert f._metadata.globalRecords[-1][0] == 'history'
    assert f._metadata.globalRecords[-1][1] == ('Testing out badc-csv code on this file',)

     # check that file is still valid and basic level compliant
    f.check_valid()

    f.check_colrefs()

    # check basic compliance
    f.check_complete(level='basic')

    # check complete compliance
    f.check_complete(level='complete')

    # check csv (should the method be called csv instead of cvs?) 
    assert f.cvs().split('\n')[0] == repr(f).split('\n')[0] == 'Conventions,G,BADC-CSV,1'
    assert f.cvs().split('\n')[-3] == repr(f).split('\n')[-3] == '2009,5,6,12,0,-9999999,2009,5,6,12,4,AIRCRAFT,TEST,44.4,11.02,1500,-9999999,-9999999,0,3,-9999999,-9999999,6,-9999999,293,2.1,-9999999,-9999999,-9999999,-9999999,279.7,-9999999,-9999999,0,-9999999,0'

    # test cdl
    assert f.cdl().split('\n')[6] == '    int var1(point);'
    assert f.cdl().split('\n')[-3] == 'var36 = 0, 0, 0, 0, 0, 0, 0, 0, 0;'


    # test NASA Ames format
    # why is there so many t's - check what is happening with this??
    assert f.NASA_Ames().split('\n')[0] == '287 1001'
    assert f.NASA_Ames().split('\n')[6] == '2009 05 06    2009 05 11 15:40'
    assert f.NASA_Ames().split('\n')[-3] == '2009 5 6 12 0 -9999999 2009 5 6 12 4 LH1852 EU0362 41.29 16.52 1500 -9999999 -9999999 0 3 -9999999 -9999999 6 -9999999 293 2.1 -9999999 -9999999 -9999999 -9999999 279.7 -9999999 -9999999 0 -9999999 0'


# test the other classes
# test with real data from mini-ceda-archive