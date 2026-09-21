# -----
# value check functions.
# each function takes a values tuple and checks it

""" BADC CSV Checker - Type Checking functions

Each Function is of the form (Tuple -> None).

To confirm that a type is VALID, nothing occurs.
To confirm that a type is INVALID, the function will throw an error.

TODO - change methods to a BOOL output True/False.
"""

import time, warnings

from badc_errors import BADCTextFileMetadataInvalid

def checkString(values):
    pass


def checkInt(values):
    for v in values:
        int(v)


def checkFloat(values):
    for v in values:
        float(v)


def checkLocation(values):
    if len(values) == 4 or len(values) == 2:
        for v in values:
            float(v)
    else:
        pass


def checkDate(values):
    # carries out a check against ISO standard date-time string
    # that conforms to one of:
    # Y-m-d
    # Y-m-d h
    # Y-m-d h:m
    # Y-m-d h:m:s
    # Y-m-d h:m:s.decimal

    for v in values:
        dateSplit = v.split(" ")
        dateString = "%Y-%m-%d"
        # print v, v.split(' ')
        if len(dateSplit) == 2:
            timeSplit = dateSplit[1].split(":")
            if len(timeSplit) == 1:
                dateString = dateString + " %H"
            if len(timeSplit) == 2:
                dateString = dateString + " %H:%M"
            if len(timeSplit) == 3:
                dateString = dateString + " %H:%M:%S"
                if "." in v:
                    dateString = dateString + ".%f"

        time.strptime(v, dateString)


def checkStandardName(values):
    pass


def checkHeight(values):
    float(values[0])


def checkFeatureType(values):
    pass


def checkCoordinateVariables(values):
    pass


def checkConventions(values):
    if values[0] != "BADC-CSV":
        raise BADCTextFileMetadataInvalid(f"Conventions must be BADC-CSV, not {values[0]}")
    if values[1] != "1":
        raise BADCTextFileMetadataInvalid(f"Conventions must be 'BADC-CSV, 1', not {values[1]}")


def MetadataInvalid(message):
    warnings.warn(message)


def checkType(values):
    v = values[0]
    if v not in ("int", "float", "char"):
        raise BADCTextFileMetadataInvalid(f"Type not right must be int, float or char. not {v}")


def checkCellMethod(values):
    pass
