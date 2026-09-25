from types import MappingProxyType

"""MDinfo defines the valid use for the metadata items in the data
files. The dictionary is keyed on the metadata label and has values
that correspond to:
    bool: A flag to say if the label can apply globally,
    bool: A flag to say if the label can apply to a column,
    int: The minimum number of values associated with the label
    int: The maximum number of values associated with the label
    int {0|1|2}: A flag to say if the label is mandatory for 'basic' files
        (0=not mandatory, 1=mandatory existence for at least one column, 2=must exist for all columns)
    int {0|1|2}: A flag to say if the label is mandatory for 'complete' files
        (0=not mandatory, 1=mandatory existence for at least one column, 2=must exist for all columns)
"""
from enum import Enum

MANDATORY_CLASS = Enum("MANDATORY_CLASS", [("NOT_MANDATORY", 0), ("MANDATORY", 1), ("ALL_COLUMNS", 2)])

mandatory_info = MappingProxyType(
    {  # Class variable is Immutable (RUF012)
        "Conventions": (1, 0, 2, 2, 1, 1, "convention", "Metadata conventions used. Must be BADC-CSV, 1"),
        "long_name": (0, 1, 2, 2, 2, 2, "string", "Description of variable and its unit"),
        "coordinate_variable": (0, 1, 0, 2, 1, 1, "coordinate", "Flag to show which column(s) are regarded as coordinate variables"),
        "creator": (1, 1, 1, 2, 0, 1, "string", "The name of the person and/or institute that created the data"),
        "source": (1, 1, 1, 1, 0, 1, "string", "The name of the tool used to produce the data. e.g. model name or instrument type"),
        "observation_station": (1, 1, 1, 1, 0, 1, "string", "The name of the observation station or instrument platform used"),
        "activity": (1, 1, 1, 1, 0, 1, "string", "The name of the activity sponsoring the collection of the data "),
        "feature_type": (1, 0, 1, 1, 0, 1, "feature_type", "type of feature,point series, trajectory or point collection"),
        "location": (1, 1, 1, 4, 0, 1, "location", "Location for the data. Can be a name, bounding box, or lat and long values"),
        "date_valid": (1, 1, 1, 2, 0, 1, "date", "The date the data is valid for. Needs to be YYYY-MM-DD form"),
        "last_revised_date": (1, 1, 1, 1, 0, 1, "date", "The date the data was revised or worked up. Needs to be YYYY-MM-DD form"),
        "history": (1, 1, 1, 1, 0, 1, "string", "Text description of the file history"),
        "standard_name": (0, 1, 3, 3, 0, 0, "standard_name", "Name of variable from a standard list, with unit and the name of the list"),
        "title": (1, 0, 1, 1, 0, 0, "string", "A title for the data file"),
        "comments": (1, 1, 1, 1, 0, 0, "string", "Any text comment associated with data"),
        "contributor": (1, 1, 1, 2, 0, 0, "string", "The name of the person and/or institute that contributed to the data"),
        "height": (1, 1, 2, 2, 0, 0, "height", "Height valid for data"),
        "reference": (1, 1, 1, 1, 0, 0, "string", "Bibliographic reference"),
        "rights": (1, 1, 1, 1, 0, 0, "string", "Conditions of use for the data"),
        "valid_min": (1, 1, 1, 1, 0, 0, "float", "Values below this value should be interpreted as missing"),
        "valid_max": (1, 1, 1, 1, 0, 0, "float", "Values above this value should be interpreted as missing"),
        "valid_range": (1, 1, 2, 2, 0, 0, "float", "Values outside this range should be interpreted as missing"),
        "type": (0, 1, 1, 1, 0, 2, "type", "The type of the variables in a column. Should be char, int or float"),
        "cell_method": (1, 1, 1, 4, 0, 0, "cell_method", "The cell method used in preparing the data"),
        "add_offset": (0, 1, 1, 1, 0, 0, "float", "An offset value to add to the values recorded in the data"),
        "scale_factor": (0, 1, 1, 1, 0, 0, "float", "A scale factor to multiply the data values by"),
        "flag_values": (0, 1, 1, 1, 0, 0, "string", "Values used for flag table in data"),
        "flag_meanings": (0, 1, 1, 1, 0, 0, "string", "Meanings for each flag_value"),
    }
)

mandatory_info_order = (
    "Conventions",
    "long_name",
    "coordinate_variable",
    "feature_type",
    "creator",
    "source",
    "observation_station",
    "location",
    "activity",
    "date_valid",
    "last_revised_date",
    "history",
    "type",
    "title",
    "comments",
    "contributor",
    "height",
    "reference",
    "rights",
    "valid_min",
    "valid_max",
    "valid_range",
    "cell_method",
    "standard_name",
    "add_offset",
    "scale_factor",
    "flag_values",
    "flag_meanings",
)
