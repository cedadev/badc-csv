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
"""

import csv
from enum import Enum
from pathlib import Path

from badc_csv.data.mandatory_info import (
    MANDATORY_CLASS,
    MandatoryClassifications,
    MandatoryLabel,
)
from badc_csv.util.error_collection import ErrorCollection

from .metadata import Metadata

COMPLIANCE_LEVEL = Enum(
    "COMPLIANCE_LEVEL",
    [
        ("NONE", 0),
        ("CSV", 1),
        ("STRUCTURE", 2),
        ("VALID_METADATA", 3),
        ("BASIC", 4),
        ("COMPLETE", 5),
        ("STANDARDISED", 6),
    ],
)


class BADC_CSV_Structure:
    def __init__(self, rows_metadata, columns, rows_data):
        self.metadata: list = rows_metadata
        self.columns: list = columns
        self.data: list = rows_data


class ComplianceChecker:
    def __init__(self):
        self.__verbose = False
        self.__disallow_warnings = False

    def set_verbose(self, setting: bool = True):
        self.__verbose = setting

    def print_verbose(self, *args, **kwargs):
        if self.__verbose:
            print("# V-LOGS:", *args, **kwargs)

    def disallow_warnings(self, setting: bool = True):
        self.__disallow_warnings = setting

    def compliance_assessment(
        self, filepath: str
    ) -> (COMPLIANCE_LEVEL, ErrorCollection):
        errors = ErrorCollection()
        # CSV Compliance
        raw, csv_errors = self.read_file(Path(filepath))
        errors += csv_errors

        if errors:
            print("Fucking hell mate")

        if self.__disallow_warnings and errors.has_warnings():
            print("you awl rite?")
            if self.__disallow_warnings:
                print("calm bruv")
            if errors.has_warnings():
                print("nuff said aight")

        if errors or (self.__disallow_warnings and errors.has_warnings()):
            self.print_verbose("CSV errors")
            for e in errors:
                self.print_verbose(e)
            return (
                COMPLIANCE_LEVEL.NONE,
                errors,
            )
        else:
            self.print_verbose("File is CSV.")  # csv is a very lax format

        # Structure Compliance
        structure, structural_errors = self.process_structure(raw)
        errors += structural_errors
        if errors or (self.__disallow_warnings and errors.has_warnings()):
            self.print_verbose("Structural errors")
            for e in structural_errors:
                self.print_verbose(e)
            return (
                COMPLIANCE_LEVEL.CSV,
                errors,
            )
        else:
            self.print_verbose("Structure Processed")

        # Valid Metadata Compliance
        metadata, metadata_errors = self.process_metadata(structure.metadata)
        column_reference_errors = metadata.columns_reference_exist(
            structure.columns
        )
        metadata_rules_errors = self.metadata_rules(metadata)
        valid_metadata_errors = (
            metadata_errors + column_reference_errors + metadata_rules_errors
        )
        errors += valid_metadata_errors
        self.print_verbose("Done with valid metadata checks")
        if errors or (self.__disallow_warnings and errors.has_warnings()):
            self.print_verbose("Metadata errors")
            for e in valid_metadata_errors:
                self.print_verbose(e)
            return (
                COMPLIANCE_LEVEL.STRUCTURE,
                errors,
            )
        else:
            self.print_verbose("Passed Valid Metadata level")

        # Basic Compliance
        basic_compliance_errors = self.basic_compliance(metadata)
        errors += basic_compliance_errors
        self.print_verbose("Done with BASIC checks")
        if errors or (self.__disallow_warnings and errors.has_warnings()):
            self.print_verbose("Basic errors")
            for e in basic_compliance_errors:
                self.print_verbose(e)
            return (
                COMPLIANCE_LEVEL.VALID_METADATA,
                errors,
            )
        else:
            self.print_verbose("Passed BASIC checks")

        # Complete Compliance
        complete_compliance_errors = self.complete_compliance(metadata)
        errors += complete_compliance_errors
        self.print_verbose("Done with COMPLETE checks")
        if errors or (self.__disallow_warnings and errors.has_warnings()):
            self.print_verbose("Complete Errors")
            for e in complete_compliance_errors:
                self.print_verbose(e)
            return (
                COMPLIANCE_LEVEL.BASIC,
                errors,
            )
        else:
            self.print_verbose("Passed COMPLETE checks")

        # TODO - Data Section Compliance (e.g. consistent # of data items per row)

        return COMPLIANCE_LEVEL.COMPLETE, errors

    def read_file(self, filepath: Path) -> (list, ErrorCollection):
        self.print_verbose(f"Path {filepath} given.")
        if not filepath.exists:
            self.print_verbose("Path does not exist. Cancelling read.")
            return None, ErrorCollection([FileExistsError(filepath)])

        self.print_verbose("Reading file.")
        with open(filepath, "r") as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            raw = [line for line in reader]
        self.print_verbose("Successful read")
        return raw, ErrorCollection()

    def process_structure(
        self, lines: list
    ) -> (BADC_CSV_Structure, ErrorCollection):
        SECTION = Enum(
            "SECTION",
            [("METADATA", 1), ("COLUMN_HEADERS", 2), ("DATA", 3), ("END", 4)],
        )

        self.print_verbose("Processing file structure.")

        def __compare_heading(expected, given) -> (bool, bool):
            """
            expected: str - heading expected
            given: str - value given
            returns exact, close: bool, bool - if matching exactly, and matching closely
            """
            exact = expected == given
            close = expected.lower() == given.lower()
            return exact, close

        errors = ErrorCollection()
        rows_metadata = []
        columns = []
        rows_data = []
        # start of section
        section = SECTION.METADATA
        self.print_verbose("Start of Metadata Section")
        for raw_row in lines:
            # ignore blank lines, whitespace
            row = [item.strip() for item in raw_row if item.strip() != ""]
            if len(row) == 0:
                continue
            # Process by section
            # SECTION: METADATA then COLUMN_HEADERS then DATA, then END
            if section == SECTION.METADATA:
                if len(row) == 1:
                    exact, close = __compare_heading("data", row[0])
                    if exact or close:
                        self.print_verbose("End of Metadata Section")
                        section = SECTION.COLUMN_HEADERS
                        if not exact:
                            errors.append(
                                f"Label must be 'data', not {row[0]}. Must be lowercase."
                            )
                        self.print_verbose("Starting Columns")
                        continue
                    else:
                        errors.append(f"Metadata malformed: {row}")
                        self.print_verbose("Stopping Early.")
                        break
                rows_metadata.append(row)  # add the metadata
                self.print_verbose("Metadata line OK -", row)
            elif section == SECTION.COLUMN_HEADERS:
                self.print_verbose(f"Columns are {row}")
                columns = [
                    colname for colname in row
                ]  # This section is only one row.
                section = SECTION.DATA
                self.print_verbose("Ending Columns")
            elif section == SECTION.DATA:
                if len(row) == 1:
                    exact, close = __compare_heading("end data", row[0])
                    if exact or close:
                        self.print_verbose("End of Data section")
                        section = SECTION.END
                        if not exact:
                            errors.append(
                                f"Label must be 'end data', not {row[0]}. Must be lowercase."
                            )
                    continue
                rows_data.append(row)
            elif section == SECTION.END:
                self.print_verbose("End of section")
                break
            else:
                errors.append(f"Invalid state reached. Row: {row} #")
                break
        return BADC_CSV_Structure(rows_metadata, columns, rows_data), errors

    def process_metadata(
        self, metadata_rows: list
    ) -> (Metadata, ErrorCollection):
        errors = ErrorCollection()
        metadata = Metadata()
        for row in metadata_rows:
            if len(row) < 3:
                errors.append(
                    f"Expects at least 3 items in each metadata row. Given: {row}"
                )
                continue
            metadata.add_row(*row)
        return metadata, errors

    def metadata_rules(self, metadata: Metadata) -> ErrorCollection:
        errors = ErrorCollection()
        mc = MandatoryClassifications()
        convention_labels = mc.get_label_names()
        # iterate through columns.
        for colname, attributes in metadata.get_attributes().items():
            attributes: dict
            for label in attributes:
                # Check metadata for controlled vocabulary
                if label in convention_labels:
                    # Reference the rules for this attribute.
                    rules: MandatoryLabel = mc.get_label(label)
                    violated_rules = rules.check_label(
                        label, colname, attributes[label]
                    )
                    errors = errors + violated_rules
        return errors

    def __check_label_compliance_at_level(
        self, metadata: Metadata, basic: bool = False, complete: bool = False
    ) -> ErrorCollection:
        errors = ErrorCollection()

        # Validation
        if not basic and not complete:
            errors.append("A compliance level must be chosen.")
            return errors
        if basic and complete:
            errors.append("Only one compliance level may be chosen.")
            return errors

        # Switch variables
        mandatory_class: str
        label_reference: list[MandatoryLabel]
        tag: str
        if basic:
            mandatory_class = "mandatory_basic"
            label_reference = MandatoryClassifications().basic_labels()
            tag = "BASIC"
        elif complete:
            mandatory_class = "mandatory_complete"
            label_reference = MandatoryClassifications().complete_labels()
            tag = "COMPLETE"

        # Check for mandatory labels
        for m_label in label_reference:
            m_label: MandatoryLabel
            if getattr(m_label, mandatory_class) == MANDATORY_CLASS.ALL_COLUMNS:
                # do ALL columns have this label?
                for (
                    column_name,
                    attributes,
                ) in metadata.get_column_attributes().items():
                    self.print_verbose(attributes.keys())
                    if m_label.label not in attributes:
                        errors.append(
                            f"CHECK '{tag}': Column '{column_name}' should have attribute '{m_label.label}'"
                        )

            elif getattr(m_label, mandatory_class) == MANDATORY_CLASS.MANDATORY:
                # is there a single column that has this label?
                has_attribute = False
                for colname, attributes in metadata.get_attributes().items():
                    self.print_verbose(attributes)
                    if m_label.label in attributes:
                        self.print_verbose(
                            f"Column '{colname}' has label '{m_label.label}'."
                        )
                        has_attribute = True
                        break  # criteria achieved, end search
                if not has_attribute:
                    message = f"CHECK {tag}: Must be at least one column with attribute: '{m_label.label}'"
                    if m_label.label == "coordinate_variable":
                        errors.add_warning(message)
                    else:
                        errors.append(message)
        return errors

    def basic_compliance(self, metadata: Metadata) -> ErrorCollection:
        return self.__check_label_compliance_at_level(metadata, basic=True)

    def complete_compliance(self, metadata: Metadata) -> ErrorCollection:
        return self.__check_label_compliance_at_level(metadata, complete=True)


"""
TODO

DATA CHECK
for each data row
- for each column
    - check that the type matches what is given, if the metadata label specifies
"""
