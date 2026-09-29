from string import whitespace

from badc_csv import ErrorCollection


class MetadataRowError(Exception):
    pass


class MetadataGlobalLabel:
    pass


class Metadata:
    def __init__(self):
        # records[column][label] = [line, ...]
        # a file has many columns.
        # a column has many attributes.
        # an attribute is described by as (label, [line])
        # a line has one (or more) comma separated values.
        self.column_names = []
        self.records = {
            MetadataGlobalLabel: {}
        }  # Example attribute. As required by format.

    def add_row(self, *args):
        # Create Metadata Row struct
        row = self.MetadataRow(*args)
        if row.errors:
            raise MetadataRowError(row.errors)  # TODO ... raise higher...

        if row.column_name not in self.records:
            # add column to record reference
            self.records[row.column_name] = {}
            self.column_names.append(row.column_name)
        record = self.records[row.column_name]

        # Enable multi-line labels
        if row.label not in record:
            record[row.label] = []
        # Treat each row as a separate label.
        record[row.label].append(row.values)

    def get_attributes(self):
        return self.records

    def get_global_attributes(self):
        return self.records[MetadataGlobalLabel]

    def get_column_attributes(self):
        return {k: self.records[k] for k in self.get_columns()}

    def get_columns(self):
        return self.column_names

    def columns_reference_exist(self, file_columns: list) -> ErrorCollection:
        errors = []
        for metadata_column in self.column_names:
            if metadata_column in file_columns:
                continue
            else:
                errors.append(
                    f"Metadata references non-existant column: {metadata_column}."
                )
        return errors

    def column_size(self) -> int:
        return len(self.records) - 1  # do not include "global" attributes.

    class MetadataRow:
        def __init__(self, label, column, *values):
            self.label, label_errors = self.verify_label(label)
            self.column_name = self.verify_column(column)
            self.values = values
            self.errors = label_errors

        def verify_label(self, label):
            errors = []
            if any(c in whitespace for c in label):
                errors.append(
                    "Labels must not contain any whitespace. Use underscore '_' for spacing."
                )
            if not label.isascii():
                errors.append(
                    f"Label contains non-ascii characters. Label: {label}."
                )

            if label.lower() != label:
                if label == "Conventions":
                    pass  # In the spec as written.
                else:
                    errors.append("Labels must be lowercase.")

            return label, errors

        def verify_column(self, column):
            if column == "G":
                return MetadataGlobalLabel
            try:
                int(column)  # check if it is an int.
                return str(
                    column
                )  # return as str, to remain consistent with reader.
            except TypeError:
                return str(column)
