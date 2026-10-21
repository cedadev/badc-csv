"""BADC CSV Checker - Type Checking functions

Each Function is of the form (Iterable -> bool).
"""

import time
from types import MappingProxyType


def __checkFloat(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def checkInt(values: list[str]) -> bool:
    for v in values:
        int(v)


def checkFloat(values: list[str]) -> bool:
    return all(__checkFloat(v) for v in values)


def checkLocation(values: list[str]) -> bool:
    if len(values) == 4 or len(values) == 2:
        return checkFloat(values)
    return True  # TODO this maintains old behaviour. Is it desired?


def checkDate(values: list[str]) -> bool:
    # carries out a check against ISO standard date-time string
    # that conforms to one of:
    # Y-m-d
    # Y-m-d h
    # Y-m-d h:m
    # Y-m-d h:m:s
    # Y-m-d h:m:s.decimal
    try:  # TODO This reduce scope of 'try, except'
        for v in values:
            dateSplit = v.split(" ")
            dateString = "%Y-%m-%d"
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
        return True
    except:  # noqa: E722
        return False


def checkHeight(values: list[str]) -> bool:
    return __checkFloat(values[0])


def checkConventions(values: list[str]) -> bool:
    # f"Conventions must be BADC-CSV, not {values[0]}"
    # f"Conventions must be 'BADC-CSV, 1', not {values[1]}"
    return values[0] == "BADC-CSV" and values[1] == "1"


def checkType(values: list[str]) -> bool:
    v = values[0]
    # f"Type not right must be int, float or char. not {v}"
    return v in ("int", "float", "char")


def getCheckFunction(expected_type: str):  # -> function (list[str] -> bool)
    def not_implemented(*args) -> bool:
        return True

    function_lookup = MappingProxyType(
        {
            "convention": checkConventions,
            "date": checkDate,
            "float": checkFloat,
            "height": checkHeight,
            "location": checkLocation,
            "type": checkType,
            # not implemented or not possible
            "cell_method": not_implemented,
            "coordinate": not_implemented,
            "feature_type": not_implemented,
            "standard_name": not_implemented,
            "string": not_implemented,
        }
    )
    return function_lookup[expected_type]
