"""Five levels of Compliance to the BADC-CSV format

0 • CSV: The file should conform to Excel dialect CSV file format. The rules
for this are fairly clear and most applications and programming languages
already support it.
1 • Structure: Data and Metadata sections exist
2 • Valid metadata: Metadata has right number of values and refers to legal
objects.
3 • Basic: Parameter names for all columns exist. This provides a file with the
same information numbers and column headings. The basic structure of
the file is correct. This level requires valid metadata.
4 • Complete: Mandatory metadata exists. Metadata should exist for some
items. Requires basic compliance.
5 • Standardised: Metadata values for appropriate is from standard list.
Requires complete compliance
"""  # noqa: N999

import csv
from enum import Enum
from pathlib import Path

from badc_csv import ErrorCollection
from badc_csv.metadata import Metadata


class BADC_CSV_Structure:
    def __init__(self, rows_metadata, columns, rows_data):
        self.metadata = rows_metadata
        self.columns = columns
        self.data = rows_data


class ComplianceChecker:
    COMPLIANCE_LEVEL = Enum("BADC_CSV_SECTION", [("NONE", 0), ("CSV", 1), ("STRUCTURE", 2), ("VALID_METADATA", 3), ("BASIC", 4), ("COMPLETE", 5), ("STANDARDISED", 6)])

    def compliance_assessment(self, filepath: str) -> (COMPLIANCE_LEVEL, ErrorCollection):
        # CSV Compliance
        raw, csv_errors = self.read_file(Path(filepath))
        if csv_errors:
            return ComplianceChecker.COMPLIANCE_LEVEL.NONE, csv_errors  # did not reach CSV compliance
        print("File is CSV.")  # csv is a very lax format

        # Structure Compliance
        structure, structural_errors = self.process_structure(raw)
        if structural_errors:
            return ComplianceChecker.COMPLIANCE_LEVEL.CSV, structural_errors  # did not reach structural compliance
        print("Structure Processed")

        # Valid Metadata Compliance
        metadata, metadata_errors = self.process_metadata(structure.metadata)
        column_reference_errors = metadata.columns_reference_exist(structure.columns)
        valid_metadata_errors = metadata_errors + column_reference_errors
        if valid_metadata_errors:
            return ComplianceChecker.COMPLIANCE_LEVEL.STRUCTURE, valid_metadata_errors

        # Basic Compliance
        # TODO ...

        # Complete Compliance
        # TODO ...

        # Additional checks (if not present already)
        ## the # of data items in each row equals the number of columns

    def read_file(self, filepath: Path) -> (list, ErrorCollection):
        if not filepath.exists:
            return None, [FileExistsError(filepath)]

        with open(filepath, "r") as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            raw = [line for line in reader]
        return raw, None

    def process_structure(self, lines: list) -> (BADC_CSV_Structure, ErrorCollection):
        SECTION = Enum("BADC_CSV_SECTION", [("METADATA", 1), ("COLUMN_HEADERS", 2), ("DATA", 3), ("END", 4)])

        def __expect_heading(expected, given) -> (bool, bool):
            """
            expected: str - heading expected
            given: str - value given
            returns exact, close: bool, bool - if matching exactly, and matching closely
            """
            exact = expected == given
            close = expected.lower() == given
            return exact, close

        errors = []
        rows_metadata = []
        columns = []
        rows_data = []
        # start of section
        section = SECTION.METADATA
        print("Start of Metadata Section")
        for raw_row in lines:
            # ignore blank lines, whitespace
            row = [item.strip() for item in raw_row if item.strip() != ""]
            if len(row) == 0:
                continue
            # Process by section
            # BADC_CSV_SECTION: METADATA then COLUMN_HEADERS then DATA, then END
            if section == SECTION.METADATA:
                if len(row) == 1:
                    exact, close = __expect_heading("data", row[0])
                    if exact or close:
                        print("End of Metadata Section")
                        section = SECTION.COLUMN_HEADERS
                        if not exact:
                            print(f"Warning: Label must be 'data', not {row[0]}. Must be lowercase.")
                        print("Starting Columns")
                        continue
                    else:
                        print("Metadata malformed:", row)
                        print("Stopping Early.")
                        break
                if rows_metadata.append(row):  # add the metadata
                    print("Metadata line OK -", row)
                    continue
                else:
                    print("Metadata malformed:", row)

            elif section == SECTION.COLUMN_HEADERS:
                for colname in row:  # This section is only one row.
                    if columns.append(colname):
                        print("Data column OK -", colname)
                    else:
                        print("Data column problem -", colname)
                section = SECTION.DATA
                print("Ending Columns")
            elif section == SECTION.DATA:
                if len(row) == 1:
                    exact, close = __expect_heading("end data", row[0])
                    if exact or close:
                        print("End of Data section")
                        section = SECTION.END
                        if not exact:
                            print(f"Warning: Label must be 'end data', not {row[0]}. Must be lowercase.")
                    continue
                rows_data.append(row)
            elif section == SECTION.END:
                print("End of section")
                break
            else:
                print("Invalid state reached. Row:", row, " #")
                break
        return BADC_CSV_Structure(rows_metadata, columns, rows_data), errors

    def process_metadata(self, metadata_rows: list) -> (Metadata, ErrorCollection):
        errors = []
        metadata = Metadata()
        for row in metadata_rows:
            if len(row) < 3:
                errors.append("Expects at least 3 items in each metadata row. Given:", row, "#")
                continue
            metadata.add_row(*row)

        return metadata, errors
