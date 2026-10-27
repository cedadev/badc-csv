# BADC CSV Evaluator

BADC Comma Separated Value Format was designed to preserve Excel type data. 

BADC-CSV format is given by the [new_ASCII_file_format_guide.md](./docs/BADC_text_file_guide.md) and also by the [badc-csv-format.pdf](./docs/badc-csv-format.pdf)


## Core Functionality

### Checker

This tool will evaluate a CSV file against the BADC-CSV standard as given.

The tool provides a level of compliance - corresponding to the 5 set out by the standard. CSV, Structure, Valid Metadata, Basic, and Complete. Then give a set of Errors that must be addressed to reach the next level. As each level in the standard requires the previous. Then a set of Warnings found at that level and all previous levels.

This report is given in JSON format.

Examples
```
uv run python -m badc_csv check tests/reference/test2.csv
uv run python -m badc_csv check tests/reference/additional/ukmo-metdb_lndsyn_20240202.csv
```

### Transformation to NetCDF

Code is available for BADC-CSV to NetCDF conversion, provided a "missing_value" label is present in the header. 

A command-line option is available, of the format below.

`uv run python -m badc_csv transform <badc_csv_file> -o <destination_netcdf_file>`
```
uv run python -m badc_csv transform tests/reference/additional/midas-open_uk-hourly-rain-obs_dv-202007_dumfriesshire_01023_eskdalemuir_qcv-1_2018.csv -o tests/tmp/test.nc
```

## Related tools

You can make BADC-CSV compliant headers using the tool provided by the following form, written by Molly Macrae.

https://github.com/mollymacrae/BADC-CSV-form
