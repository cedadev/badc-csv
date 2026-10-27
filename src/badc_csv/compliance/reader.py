from pathlib import Path

from .metadata import Metadata


def read_metadata(
    variable_columns: list[str], metadata_rows: list[str]
) -> Metadata:
    metadata_lines = [l.split(",") for l in metadata_rows]
    # interpret metadata
    metadata = Metadata()
    for row in metadata_lines:
        metadata.add_row(*row)  # if non-compliance, allow it to raise exception
    assert set(variable_columns) == set(
        metadata.get_columns()
    )  # columns should match! order does not matter
    return metadata


class BADC_Data:
    def __init__(self, columns, rows: list[list]):
        self.columns: tuple[str] = tuple(col for col in columns)
        self.data_rows: tuple[tuple] = tuple(
            tuple(datum for datum in row) for row in rows
        )
        self.size: int = len(rows)
        self.data_by_column_name: dict[str:list] = self.__set_data_by_column(
            columns, self.data_rows
        )

    def __len__(self):
        return self.size

    def __set_data_by_column(self, columns, rows) -> dict[str:list]:
        data: dict[str:list] = {col_name: [] for col_name in columns}
        for row in rows:
            for col_name, datum in zip(columns, row):
                data[col_name].append(datum)
        return data

    def get_row(self, index: int) -> tuple:
        return self.data_rows[index]

    def get_column_by_name(self, name: str) -> tuple:
        return self.data_by_column_name[name]

    def get_column_by_index(self, index: int) -> tuple:
        return self.data_by_column_name[self.columns[index]]


def read_data(variable_columns: list[str], data_rows: list[str]) -> BADC_Data:
    data_lines = [l.split(",") for l in data_rows]
    data = BADC_Data(variable_columns, data_lines)
    return data


def reader(file: Path) -> (Metadata, BADC_Data):
    """Take a BADC CSV filepath,
    return a representation of the file
    """
    # Read file
    with open(file, "r") as f:
        lines: list[str] = f.read().splitlines()
    # Get indicies
    data_line_index: int = lines.index("data")
    metadata_end_line_index: int = data_line_index
    variable_columns_lines_index: int = data_line_index + 1
    data_start_line_index: int = variable_columns_lines_index + 1
    enddata_line_index: int = lines.index("end data")

    # Metadata
    metadata_lines = lines[:metadata_end_line_index]
    variable_columns = lines[variable_columns_lines_index].split(",")
    metadata = read_metadata(variable_columns, metadata_lines)
    # Data
    data_rows = lines[data_start_line_index:enddata_line_index]
    data = read_data(variable_columns, data_rows)

    return metadata, data
