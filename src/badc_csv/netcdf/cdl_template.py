# Using NetCDF user guide as reference for CDL
# https://docs.unidata.ucar.edu/nug/2.0-draft/cdl.html

# Example given by page (tab delimited)
"""netcdf example {   // example of CDL notation
    dimensions:
        lon = 3 ;
        lat = 8 ;
        time = unlimited ;
    variables:
        float lon(lon) ;
            lon:units = "degrees_north" ;
            lon:long_name = "longitude" ;
        float lat(lat) ;
            lat:units = "degrees_east" ;
            lat:long_name = "latitude" ;
        float time(time) ;
            time:units = "seconds since 1992-1-1 00:00:00" ;
        float rh(time, lon, lat) ;
            rh:units = "percent" ;
            rh:long_name = "Relative humidity" ;
    // global attributes
    :title = "Simple example" ;

    data:
        lon = -120, -105, -90 ;
        lat = 10, 20, 30, 40, 50, 60, 70, 80 ;
        time = 0, 180 ;
        rh =
            2, 3, 5, 7, 11, 13, 17, 19,
            23, 29, 31, 37, 41, 43, 47, 53,
            59, 61, 67, 71, 73, 79, 83, 89,
            1, 3, 4, 7, 9, 11, 13, 15,
            16, 17, 19, 21, 23, 25, 27, 29,
            31, 33, 35, 37, 39, 41, 43, 45 ;
}
"""


class CDL_Templates:
    # CDL. One dimension. Tab (`\t`) delimited.
    # NB double curly braces '{{}}', used to escape f-string to put in '{' as text
    # see docs - https://peps.python.org/pep-0498/#escape-sequences
    # NB multiline text includes indentation. (non-indent is intentional)
    CDL_TEMPLATE_ONE_DIMENSION = """netcdf {filename} {{
\tdimensions:
{dimensions_size_declarations_inc_tabs}
\tvariables:
{all_variables_lines_inc_tabs}
\t// global attributes
{all_global_attribute_lines_inc_tabs}

\tdata:
// maybe declare dimension(s) here? Not sure.
{all_data}
}}
"""
    # Dimensions
    DIMENSION_LINE_TEMPLATE = "\t\t{name} = {count} ;"
    # Variables
    VARIABLE_DECLARATION_TEMPLATE = "\t{type} {name}({indexed_on}) ;"
    VARIABLE_ATTRIBUTE_TEMPLATE = "\t\t{name}:{attribute} = {value} ;"
    # Globals
    GLOBAL_ATTRIBUTE_LINE_TEMPLATE = '\t:{attribute} = "{value}" ;'
    # Data
    DATA_LINE_TEMPLATE = "\t\t{variable_name} = {data_values_comma_separated} ;"  # Whitespace in the "data_values..." is ignored. i.e. newlines are acceptable!
