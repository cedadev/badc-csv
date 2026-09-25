from string import whitespace

from badc_csv import ErrorCollection


class MetadataGlobalLabel:
    pass


class Metadata:
    def __init__(self):
        self.global_records = []
        self.columns = []  # Excludes global attributes
        self.records = {}  # Excludes global attributes

    def add_row(self, *args):
        row = self.MetadataRow(*args)
        if row.column == MetadataGlobalLabel:
            self.global_records.append((row.label, row.values))
            return
        if row.label not in self.columns:
            self.columns.append(row.label)
            self.records[row.column] = {}
        record = self.records[row.column]
        if row.label not in record:
            record[row.label] = []  # enables repeated lines to describe a single entry
        record[row.label].append(row.values)
        return

    def columns_reference_exist(self, file_columns: list) -> ErrorCollection:
        errors = []
        for metadata_column in self.columns:
            if metadata_column in file_columns:
                continue
            else:
                errors.append(f"Metadata references non-existant column: {metadata_column}.")

    def column_size(self) -> int:
        return len(self.columns)

    class MetadataRow:
        def __init__(self, label, column, *values):
            self.label, label_errors = self.verify_label(label)
            self.column = self.verify_column(column)
            self.values = values
            self.errors = label_errors

        def verify_label(label):
            errors = []
            if any(c in whitespace for c in label):
                errors.append("Labels must not contain any whitespace. Use underscore '_' for spacing.")

            if label.lower() != label:
                errors.append("Labels must be lowercase.")

            return label, errors

        def verify_column(column):
            if column == "G":
                return MetadataGlobalLabel
            try:
                return int(column)
            except TypeError:
                return str(column)

    class MetadataColumn:
        def __init__(self, name, value): ...
