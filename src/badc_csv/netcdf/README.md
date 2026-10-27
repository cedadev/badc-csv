# README


## BADC-CSV to NetCDF Conversion

### Missing and Fill values

While the BADC-CSV spec does not require a label for "missing_value", the conversion process to NetCDF requires one.

### Data loss during conversion

As the BADC CSV is a text-based format and NetCDF4 is binary, there will be some approximation of data during encoding-decoding between formats.

Some numbers, particularly floating point values, cannot be represented with the same accuracy in text versus binary formats.

If the dataset requires a high degree of precision (e.g. 7+ sf), then additional considerations should be made.

### Limitations of Data types

The only given "data" types that are explicitly given for BADC-CSV files are "int, float, char". These underspecify the available datatypes in NetCDF.

This tool therefore encodes dates as strings by default (unless it has already been encoded as numeric).

## Future Work

Proposed extensions to the BADC-CSV to NetCDF conversion tool.

### ENUM Detection during NETCDF Generation.

Some values, particularly in spreadsheets, may restrict a column to a set of key-words. Normally "word"s are not allowed in NetCDF data -- as it requires fixed-size encodings. But by detecting these values, they can be converted to ENUMs and encoded as a number indicating which value it refers to (with the relevant metadata generated).


### Use of spec-defined 'coordinate variable'

Use **the** coordinate variable as the index dimension. It is currently not used in conversion. 
