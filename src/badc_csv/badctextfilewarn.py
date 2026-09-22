# This module is for reading and writing the simple BADC text file format.
# This file format is based on the common separated value (CSV) format that
# is commonly produced by spreadsheet applications. It also checks to see if
# certain metadata is available.
#
# SJP 2008-09-22

import csv
import io
import sys
from enum import Enum
from types import MappingProxyType

from badc_csv.badc_errors import BADCTextFileError
from badc_csv.check_types import *  # TODO bad style

BADC_CSV_SECTION = Enum("BADC_CSV_SECTION", [("METADATA", 1), ("COLUMN_HEADERS", 2), ("DATA", 3), ("END", 4)])

MANDATORY_CLASS = Enum("MANDATORY_CLASS", [("NOT_MANDATORY", 0), ("MANDATORY", 1), ("ALL_COLUMNS", 2)])


class BADCTextFile:
    """The BADCTextFile class is the main class for manipulating data.

    MDinfo defines the valid use for the metadata items in the data
    files. The dictionary is keyed on the metadata label and has values
    that correspond to:
      A flag to say if the label can apply globally,
      A flag to say if the label can apply to a column,
      The minimum number of values associated with the label
      The maximum number of values associated with the label
      A flag to say if the label is mandatory for 'basic' files
          (0=not mandatory, 1=mandatory existence for at least one column, 2=must exist for all columns)
      A flag to say if the label is mandatory for 'complete' files
          (0=not mandatory, 1=mandatory existence for at least one column, 2=must exist for all columns)
    """

    MDinfo = MappingProxyType(
        {  # Class variable is Immutable (RUF012)
            "Conventions": (1, 0, 2, 2, 1, 1, checkConventions, "Metadata conventions used. Must be BADC-CSV, 1"),
            "long_name": (0, 1, 2, 2, 2, 2, checkString, "Description of variable and its unit"),
            "coordinate_variable": (0, 1, 0, 2, 1, 1, checkCoordinateVariables, "Flag to show which column(s) are regarded as coordinate variables"),
            "creator": (1, 1, 1, 2, 0, 1, checkString, "The name of the person and/or institute that created the data"),
            "source": (1, 1, 1, 1, 0, 1, checkString, "The name of the tool used to produce the data. e.g. model name or instrument type"),
            "observation_station": (1, 1, 1, 1, 0, 1, checkString, "The name of the observation station or instrument platform used"),
            "activity": (1, 1, 1, 1, 0, 1, checkString, "The name of the activity sponsoring the collection of the data "),
            "feature_type": (1, 0, 1, 1, 0, 1, checkFeatureType, "type of feature,point series, trajectory or point collection"),
            "location": (1, 1, 1, 4, 0, 1, checkLocation, "Location for the data. Can be a name, bounding box, or lat and long values"),
            "date_valid": (1, 1, 1, 2, 0, 1, checkDate, "The date the data is valid for. Needs to be YYYY-MM-DD form"),
            "last_revised_date": (1, 1, 1, 1, 0, 1, checkDate, "The date the data was revised or worked up. Needs to be YYYY-MM-DD form"),
            "history": (1, 1, 1, 1, 0, 1, checkString, "Text description of the file history"),
            "standard_name": (0, 1, 3, 3, 0, 0, checkStandardName, "Name of variable from a standard list, with unit and the name of the list"),
            "title": (1, 0, 1, 1, 0, 0, checkString, "A title for the data file"),
            "comments": (1, 1, 1, 1, 0, 0, checkString, "Any text comment associated with data"),
            "contributor": (1, 1, 1, 2, 0, 0, checkString, "The name of the person and/or institute that contributed to the data"),
            "height": (1, 1, 2, 2, 0, 0, checkHeight, "Height valid for data"),
            "reference": (1, 1, 1, 1, 0, 0, checkString, "Bibliographic reference"),
            "rights": (1, 1, 1, 1, 0, 0, checkString, "Conditions of use for the data"),
            "valid_min": (1, 1, 1, 1, 0, 0, checkFloat, "Values below this value should be interpreted as missing"),
            "valid_max": (1, 1, 1, 1, 0, 0, checkFloat, "Values above this value should be interpreted as missing"),
            "valid_range": (1, 1, 2, 2, 0, 0, checkFloat, "Values outside this range should be interpreted as missing"),
            "type": (0, 1, 1, 1, 0, 2, checkType, "The type of the variables in a column. Should be char, int or float"),
            "cell_method": (1, 1, 1, 4, 0, 0, checkCellMethod, "The cell method used in preparing the data"),
            "add_offset": (0, 1, 1, 1, 0, 0, checkFloat, "An offset value to add to the values recorded in the data"),
            "scale_factor": (0, 1, 1, 1, 0, 0, checkFloat, "A scale factor to multiply the data values by"),
            "flag_values": (0, 1, 1, 1, 0, 0, checkString, "Values used for flag table in data"),
            "flag_meanings": (0, 1, 1, 1, 0, 0, checkString, "Meanings for each flag_value"),
        }
    )

    MDinfoOrder = (  # This is not used. Should it be?
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

    def __init__(self, fh):
        self.fh = fh
        self.version = 1
        self._data = BADCTextFileData()
        self._metadata = BADCTextFileMetadata()
        if self.fh.mode == "r":
            self.parse()
        else:
            self.add_metadata("Conventions", ("BADC-CSV", "1"), "G")

    def parse(self):
        reader = csv.reader(self.fh)
        section = BADC_CSV_SECTION.METADATA
        for raw_row in reader:
            # ignore blank lines, and remove whitespace
            row = [item for item in raw_row if item != ""]
            if len(row) == 0:
                continue
            # Process by section
            # BADC_CSV_SECTION: METADATA then COLUMN_HEADERS then DATA, then END
            if section == BADC_CSV_SECTION.METADATA:
                try:
                    if len(row) >= 3:
                        label, ref, raw_values = row[0], row[1], row[2:]  # This can raise an error
                        # At least 1 item in "values" is expected
                        values = tuple(v.strip() for v in raw_values)
                        self.add_metadata(label, values, ref)  # cannot raise an error...
                    elif len(row) == 1 and row[0].lower() == "data":
                        section = BADC_CSV_SECTION.COLUMN_HEADERS
                        continue
                    else:
                        raise BADCTextFileError(f'Expected metadata entry (3+ comma separated values), or "data" (end of section). Instead got: {row}')

                except BADCTextFileError:
                    print(f"Error in section {BADC_CSV_SECTION.METADATA}, METADATA")
                    raise
            elif section == BADC_CSV_SECTION.COLUMN_HEADERS:
                # This section is only one row.
                for colname in row:
                    try:
                        self.add_variable(colname)
                    except BADCTextFileError:
                        print(f"Error in section {BADC_CSV_SECTION.COLUMN_HEADERS}, COLUMN_HEADERS")
                        raise
                section = BADC_CSV_SECTION.DATA
            elif section == BADC_CSV_SECTION.DATA:
                try:
                    if len(row) == 1 and row[0].lower() == "end data":
                        section = BADC_CSV_SECTION.END
                        continue
                    self.add_datarecord(row)
                except BADCTextFileError:
                    print(f"Error in section {BADC_CSV_SECTION.DATA}, DATA")
                    raise

            if section == BADC_CSV_SECTION.END:
                return

    def check_valid(self):
        for label in BADCTextFile.MDinfoOrder:
            global_label, column_label, min_count, max_count, _, _, validationFunction, _ = BADCTextFile.MDinfo[label]
            global_label: bool
            column_label: bool
            min_count: int
            max_count: int

            # if label can't apply globally but is defined raise error
            if not global_label and self[label] != []:
                MetadataInvalid(f"Not allowed as global metadata parameter: {label}, {self[label]}")
            # if label can't apply to column but is defined raise error
            if not column_label and self[label] == []:
                for colname in self.colnames():
                    if self[label, colname] != []:
                        MetadataInvalid(f"Given metadata not allowed for a column: {label}, {colname}, {self[label, colname]}")
            # values have wrong number of fields
            for values in self[label]:
                if len(values) > max_count:
                    MetadataInvalid(f"Max number of metadata fields ({max_count}) exceeded for {label}: {values}")
                if len(values) < min_count:
                    MetadataInvalid(f"Min number of metadata fields ({min_count}) not given for {label}: {values}")
            for colname in self.colnames():
                for values in self[label, colname]:
                    if len(values) > max_count:
                        MetadataInvalid(f"Max number of metadata fields ({max_count}) exceeded for column:{colname} {label}: {values}")
                    if len(values) < min_count:
                        MetadataInvalid(f"Min number of metadata fields ({min_count}) not given for column:{colname} {label}: {values}")

            # see if values are OK
            for values in self[label]:
                if validationFunction(values) == False:
                    MetadataInvalid(f"Metadata field values invalid {label}: {values}  [{sys.exc_info()[1]}]")
            for colname in self.colnames():
                for values in self[label, colname]:
                    if validationFunction(values) == False:
                        MetadataInvalid(f"Metadata field values for column '{colname}' invalid {label}: {values}  [{sys.exc_info()[1]}]")

    def check_colRefs(self):
        metadataRefs = list(set(line[1] for line in self._metadata.varRecords))  # noqa: C401
        long_namesCnt = tuple(colname for colname in set(self.colnames()) if colname != "G")

        if len(long_namesCnt) == len(metadataRefs):
            for colName in long_namesCnt:
                if not colName in metadataRefs:
                    metadata_entries = ",".join(metadataRefs)
                    MetadataInvalid(f"Column name {colName} not used as reference to connect metadata entries {metadata_entries}")
                    break  # Here to mirror previous behaviour. I would remove.
        else:
            header_references = ",".join(metadataRefs)
            column_headings = ",".join(self.colnames())
            MetadataInvalid(f"Not all column headings given. Header references are: {header_references}\nColumn headings given are: {column_headings}")

    def check_complete(self, level="basic"):
        self.check_colRefs()
        self.check_valid()
        for label in BADCTextFile.MDinfoOrder:
            global_label, column_label, _, _, mandatory_basic, mandatory_complete, _, _ = BADCTextFile.MDinfo[label]
            global_label: bool
            column_label: bool
            mandatory: MANDATORY_CLASS
            mandatory_basic: MANDATORY_CLASS
            mandatory_complete: MANDATORY_CLASS

            if level not in ("basic", "complete"):
                level = "complete"

            # find level for check
            if level == "basic":
                mandatory = mandatory_basic
            if level == "complete":
                mandatory = mandatory_complete

            # if its not mandatory skip
            if not mandatory:
                continue

            # if applies globally then there should be a global record or
            # one at least one variable
            if global_label and column_label:
                if self[label] != []:
                    # found global value. next label
                    continue
                for colname in self.colnames():
                    if self[label, colname] != []:
                        break
                else:
                    if mandatory == mandatory_basic:
                        MetadataInvalid(f"Mandatory basic global/column metadata not provided: {label}")
                    elif mandatory == mandatory_complete:
                        MetadataInvalid(f"Recommended complete global/column metadata not provided: {label}")
                    else:
                        MetadataInvalid(f"Suggested global/column metadata not provided: {label}")
            elif global_label and not column_label:
                if self[label] != []:
                    # found global value. next label
                    continue
                for colname in self.colnames():
                    if self[label, colname] != []:
                        break
                else:
                    if mandatory == mandatory_basic:
                        MetadataInvalid(f"Mandatory global metadata not provided: {label}")
                    elif mandatory == mandatory_complete:
                        MetadataInvalid(f"Recommended complete global metadata not provided: {label}")
                    else:
                        MetadataInvalid(f"Suggested global metadata not provided: {label}")

                # if applies to column only then there should be a record for each variable
            elif column_label and mandatory == MANDATORY_CLASS.ALL_COLUMNS:
                for colname in self.colnames():
                    if self[label, colname] == []:
                        MetadataInvalid(f'Recommended complete column metadata "{label}" for column {colname} missing')

    def colnames(self):
        return tuple(self._data.colnames)

    def nvar(self):
        return self._data.nvar()

    def __len__(self):
        return len(self._data)

    def __getitem__(self, i):
        # -- ref change
        if type(i) == int:
            return self._data[i]
        else:
            return self._metadata[i]

    def add_variable(self, colname, data=()):
        # -- ref change
        self._data.add_variable(colname, data)

    def add_datarecord(self, datavalues):
        self._data.add_data_row(datavalues)

    def add_metadata(self, label, values, ref="G"):
        self._metadata.add_record(label, values, ref)

    def __repr__(self):
        return self.cvs()

    def cdl(self):
        # create a CDL file (to make NetCDF)
        s = "// This CDL file was generated from a BADC text file file\n"
        s = s + "netcdf foo { \n"

        s = s + f"dimensions:\n   point = {len(self)};\n\n"

        s = s + "variables: \n"
        for colname in self.colnames():
            varname = f"var{colname}"
            vartype = self["type", colname][0][0]
            s = s + "    " + f"{vartype} {varname}(point);\n"
        s = s + "\n"

        s = s + self._metadata.cdl()
        s = s + "\n"

        s = s + "data:\n"
        for i in range(self.nvar()):
            varname = f"var{self._data.colnames[i]}"
            values = ", ".join(self[i])
            s = s + f"{varname} = {values};\n"
        s = s + "}\n"

        return s

    def cvs(self):  # TODO change interface because of spelling mistake -> csv.
        s = io.StringIO()
        cvswriter = csv.writer(s, lineterminator="\n")
        self._metadata.csv(cvswriter)
        self._data.csv(cvswriter)
        return s.getvalue()


class BADCTextFileData:
    # class to hold data in the files
    # BADCTextFileData is an aggregation of variables
    def __init__(self):
        self.variables = []
        self.colnames = []

    def add_variable(self, name, values):
        if len(self.variables) == 0 or len(values) == len(self.variables[0]):
            self.variables.append(BADCTextFileVariable(values))
            self.colnames.append(name)
        else:
            raise BADCTextFileError("Wrong length of data")

    def add_data_row(self, values):
        if self.nvar() == 0 and len(values) != 0:
            for v in values:
                self.variables.append(BADCTextFileVariable((v,)))
        elif self.nvar() == len(values):
            for i in range(len(values)):
                self.variables[i].append(values[i])
        else:
            raise BADCTextFileError("Wrong length of data")

    def __len__(self):
        # number of data rows
        if len(self.variables) == 0:
            return 0
        return len(self.variables[0])

    def nvar(self):
        return len(self.variables)

    def __getitem__(self, i):
        if type(i) == int:
            return self.variables[i].values
        else:
            col, row = i
            return self.variables[col][row]

    def getrow(self, i):
        row = []
        for j in range(self.nvar()):
            row.append(self.variables[j][i])
        return row

    def csv(self, csvwriter):
        csvwriter.writerow(("Data",))
        csvwriter.writerow(self.colnames)
        for i in range(len(self)):
            csvwriter.writerow(self.getrow(i))
        csvwriter.writerow(("End Data",))


class BADCTextFileVariable:
    # class to hold 1D data.
    def __init__(self, values=()):
        self.set_values(values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, i):
        return self.values[i]

    def append(self, v):
        self.values.append(v)

    def set_values(self, values):
        self.values = list(values)


class BADCTextFileMetadata:
    def __init__(self):
        # records in label, value form. Where label is the metadata label e.g. title and value is a tuple
        # e.g. ("my file",)
        self.globalRecords = []
        self.varRecords = []

    def __getitem__(self, i):
        # if the item is selected with a label and a column name then
        # use get the metadata record for the column. otherwise use expect the
        # metadata label for global
        val = []
        if type(i) == tuple:
            lab, col = i
            #  for label, value in self.globalRecords:
            #      if lab ==label:
            #          val.append(value)

            for label, column, value in self.varRecords:
                if lab == label and col == column:
                    val.append(value)
        else:
            lab = i
            for label, value in self.globalRecords:
                if lab == label:
                    val.append(value)
        return val

    def add_record(self, label, values, ref="G"):
        if type(values) != tuple:
            values = (values,)
        if type(ref) == str and ref == "G":
            self.globalRecords.append((label, values))
        elif type(ref) == str:
            self.varRecords.append((label, ref, values))

    def cdl(self):
        # return cdl representation of metadata
        s = "// variable attributes\n"
        # make sure labels are unique for netCDF. e.g. creator, creator1, creator2
        used_labels = {}
        for label, column, values in self.varRecords:
            if (label, column) in used_labels:
                use_label = f"{label}{used_labels[label, column]}"
                used_labels[label, column] = used_labels[label, column] + 1
            else:
                use_label = label
                used_labels[label, column] = 1
            value = ", ".join(values)
            s = s + f'        var{column}:{use_label} = "{value}";\n'

        s = s + "// global attributes\n"
        used_labels = {}
        for label, values in self.globalRecords:
            if label in used_labels:
                use_label = f"{label}{used_labels[label]}"
                used_labels[label] = used_labels[label] + 1
            else:
                use_label = label
                used_labels[label] = 1
            value = ", ".join(values)
            s = s + f'        :{use_label} = "{value}";\n'
        return s

    def csv(self, csvwriter):
        for label, values in self.globalRecords:
            csvwriter.writerow((label, "G") + values)
        for label, ref, values in self.varRecords:
            csvwriter.writerow((label, ref) + values)
