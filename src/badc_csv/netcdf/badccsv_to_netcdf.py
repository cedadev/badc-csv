from pathlib import Path

import netCDF4 as nc
import numpy as np

from badc_csv.compliance.reader import reader

ENCODING = "utf-8"

netcdf_type_mapping = {  # some defaults
    "char": "S1",  # This refers to a single character.
    "int": "i4",  # 4 byte integer
    "float": "f4",  # 4 byte floating point
}
netcdf_type_fill_value = {
    "char": "",
    "int": 999999,
    "float": 999999.0,
}


def _attributes_to_dict(attributes) -> dict:
    return {
        attribute: " ".join(" ".join(section) for section in values)
        for attribute, values in attributes.items()
    }


def convert_badccsv_to_netcdf(badc_csv_file: Path, nc_file: Path):
    # Read File
    metadata, data = reader(badc_csv_file)
    with nc.Dataset(nc_file, "w", format="NETCDF4") as ds:
        # Global Attributes
        global_attributes = _attributes_to_dict(
            metadata.get_global_attributes()
        )
        missing_value = global_attributes["missing_value"]
        for label, value in global_attributes.items():
            setattr(ds, label, value)

        # Generate Array for String Encoding
        def to_char_array(values, enc=ENCODING) -> tuple[np.array, int]:
            encoded = [
                ("" if v is None or v == missing_value else str(v)).encode(enc)
                for v in values
            ]
            width = max(1, max((len(b) for b in encoded), default=1))
            arr = np.array(encoded, dtype=f"S{width}")
            return arr, width

        # Dimensions
        index_name = "index"
        index_variable = ds.createDimension(index_name, data.size)  # noqa: F841

        # Variables
        for column in metadata.get_columns():
            # Create variable, with type information
            col_type = metadata.get_column_type(column)
            netcdf_type = netcdf_type_mapping[col_type]
            fill_value = netcdf_type_fill_value[col_type]

            # Get dimensions + data.
            # Different for char/string types (implicit arrays)
            if col_type == "char":
                column_char_array, str_column_width = to_char_array(
                    data.get_column_by_name(column)
                )
                data_source = nc.stringtochar(column_char_array)
                # generate a new dimension for each column of 'char' type
                char_index = ds.createDimension(
                    f"{column}_strlen", str_column_width
                )
                dimensions = (index_name, char_index)
            else:
                dimensions = (index_name,)
                data_source = [
                    val if val != missing_value else fill_value
                    for val in data.get_column_by_name(column)
                ]

            # Create Variable
            v = ds.createVariable(
                column,
                netcdf_type,
                dimensions=dimensions,
                fill_value=fill_value,
            )
            if col_type == "char":
                v._Encoding = ENCODING

            # Populate data into dataset
            v[:] = data_source

            # Fill out Variable Attributes
            attributes = metadata.get_column_attributes(column)
            for label, value in _attributes_to_dict(attributes).items():
                setattr(v, label, value)

            # Units
            if "units" not in attributes:
                v.units = "Unknown"


if __name__ == "__main__":
    # BADC CSV file that passes "Complete"
    badc_csv_file = "tests/reference/additional/midas-open_uk-hourly-rain-obs_dv-202007_dumfriesshire_01023_eskdalemuir_qcv-1_2018.csv"
    # NetCDF Destination
    nc_file = "tests/tmp/test.nc"
    # Demo conversion
    convert_badccsv_to_netcdf(badc_csv_file, nc_file)
