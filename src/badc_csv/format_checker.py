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

from badc_csv import ErrorCollection
from badc_csv.mandatory_info import (
    MANDATORY_CLASS,
    MandatoryClassifications,
    MandatoryLabel,
)
from badc_csv.metadata import Metadata, MetadataGlobalLabel


class BADC_CSV_Structure:
    def __init__(self, rows_metadata, columns, rows_data):
        self.metadata: list = rows_metadata
        self.columns: list = columns
        self.data: list = rows_data


class ComplianceChecker:
    COMPLIANCE_LEVEL = Enum(
        "BADC_CSV_SECTION",
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

    def __init__(self):
        self.__verbose = False

    def set_verbose(self, setting: bool = True):
        self.__verbose = setting

    def print_verbose(self, *args, **kwargs):
        if self.__verbose:
            print("# V-LOGS:", *args, **kwargs)

    def compliance_assessment(
        self, filepath: str
    ) -> (COMPLIANCE_LEVEL, ErrorCollection):
        # CSV Compliance
        raw, csv_errors = self.read_file(Path(filepath))
        if csv_errors:
            for e in csv_errors:
                print(e)
            return (
                ComplianceChecker.COMPLIANCE_LEVEL.NONE,
                csv_errors,
            )
        print("File is CSV.")  # csv is a very lax format

        # Structure Compliance
        structure, structural_errors = self.process_structure(raw)
        if structural_errors:
            for e in structural_errors:
                print(e)
            return (
                ComplianceChecker.COMPLIANCE_LEVEL.CSV,
                structural_errors,
            )
        print("Structure Processed")

        # Valid Metadata Compliance
        metadata, metadata_errors = self.process_metadata(structure.metadata)
        column_reference_errors = metadata.columns_reference_exist(
            structure.columns
        )
        metadata_rules_errors = self.metadata_rules(metadata)
        valid_metadata_errors = (
            metadata_errors + column_reference_errors + metadata_rules_errors
        )
        self.print_verbose("Done with valid metadata checks")
        if valid_metadata_errors:
            for e in valid_metadata_errors:
                print(e)
            # return (
            #     ComplianceChecker.COMPLIANCE_LEVEL.STRUCTURE,
            #     valid_metadata_errors,
            # )
        else:
            print("Passed Valid Metadata level")

        # Basic Compliance
        basic_compliance_errors = self.basic_compliance(metadata)
        self.print_verbose("Done with BASIC checks")
        if basic_compliance_errors:
            for e in basic_compliance_errors:
                print(e)
            # return (
            #     ComplianceChecker.COMPLIANCE_LEVEL.VALID_METADATA,
            #     basic_compliance_errors,
            # )
        else:
            print("Passed BASIC checks")

        # Complete Compliance
        complete_compliance_errors = self.complete_compliance(metadata)
        self.print_verbose("Done with COMPLETE checks")
        if complete_compliance_errors:
            for e in complete_compliance_errors:
                print(e)
            # return (
            #     ComplianceChecker.COMPLIANCE_LEVEL.VALID_METADATA,
            #     complete_compliance_errors,
            # )
        else:
            print("Passed COMPLETE checks")

        # TODO - Data Section Compliance (e.g. consistent # of data items per row)

        compliance_level = ComplianceChecker.COMPLIANCE_LEVEL.COMPLETE
        if complete_compliance_errors:
            compliance_level = ComplianceChecker.COMPLIANCE_LEVEL.BASIC
        if basic_compliance_errors:
            compliance_level = ComplianceChecker.COMPLIANCE_LEVEL.VALID_METADATA
        if valid_metadata_errors:
            compliance_level = ComplianceChecker.COMPLIANCE_LEVEL.STRUCTURE

        total_errors = (
            valid_metadata_errors
            + basic_compliance_errors
            + complete_compliance_errors
        )
        return compliance_level, total_errors

    def read_file(self, filepath: Path) -> (list, ErrorCollection):
        self.print_verbose(f"Path {filepath} given.")
        if not filepath.exists:
            self.print_verbose("Path does not exist. Cancelling read.")
            return None, [FileExistsError(filepath)]

        self.print_verbose("Reading file.")
        with open(filepath, "r") as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            raw = [line for line in reader]
        self.print_verbose("Successful read")
        return raw, []

    def process_structure(
        self, lines: list
    ) -> (BADC_CSV_Structure, ErrorCollection):
        SECTION = Enum(
            "BADC_CSV_SECTION",
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

        errors = []
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
            # BADC_CSV_SECTION: METADATA then COLUMN_HEADERS then DATA, then END
            if section == SECTION.METADATA:
                if len(row) == 1:
                    exact, close = __compare_heading("data", row[0])
                    if exact or close:
                        self.print_verbose("End of Metadata Section")
                        section = SECTION.COLUMN_HEADERS
                        if not exact:
                            errors.append(
                                f"Warning: Label must be 'data', not {row[0]}. Must be lowercase."
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
                                f"Warning: Label must be 'end data', not {row[0]}. Must be lowercase."
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
        errors = []
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
        errors = []
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

                    # Global flag, Column flag
                    if colname is MetadataGlobalLabel:  # column is "Global"
                        if (
                            not rules.global_flag
                        ):  # global must have global flag
                            errors.append(f"Global cannot have label {label}.")
                    elif (
                        not rules.column_flag
                    ):  # specific column / non-global must have column flag
                        errors.append(
                            f"Non-global column cannot have label {label}."
                        )

                    # Number of "values" in a label
                    num_values = len(attributes[label])
                    if not (
                        rules.min_count <= num_values <= rules.max_count
                    ):  # Unclear how this should be implemented for multiple lines.
                        errors.append(
                            f"For label {label} column {colname}: Number of values must be between {rules.min_count} and {rules.max_count} (inc). Instead got {num_values}."
                        )

                    # Check that the label values (of the metadata) are correctly typed
                    type_check_result: bool = rules.type_check(
                        attributes[label]
                    )
                    if not type_check_result:
                        errors.append(
                            f"TypeCheck error for label {label} on column {colname}. Expected type {rules.expected_type}."
                        )
        return errors

    def __check_label_compliance_at_level(
        self, metadata: Metadata, basic: bool = False, complete: bool = False
    ) -> ErrorCollection:
        errors = []

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
                            f"CHECK {tag}: Column {column_name} should have attribute {m_label.label}"
                        )

            elif getattr(m_label, mandatory_class) == MANDATORY_CLASS.MANDATORY:
                # is there a single column that has this label?
                has_attribute = False
                for colname, attributes in metadata.get_attributes().items():
                    self.print_verbose(attributes)
                    if m_label.label in attributes:
                        self.print_verbose(
                            f"Column {colname} has label {m_label.label}."
                        )
                        has_attribute = True
                        break  # criteria achieved, end search
                if not has_attribute:
                    errors.append(
                        f"CHECK {tag}: Must be at least one column with attribute: {m_label.label}"
                    )
        return errors

    def basic_compliance(self, metadata: Metadata) -> ErrorCollection:
        return self.__check_label_compliance_at_level(metadata, basic=True)

    def complete_compliance(self, metadata: Metadata) -> ErrorCollection:
        return self.__check_label_compliance_at_level(metadata, complete=True)


"""
COLUMN CHECK
for each column
- check that it has a name!


DATA CHECK
for each data row
- for each column
    - check that the type matches what is given, if the metadata label specifies

"""
