# BADC CSV Evaluator

BADC Comma Separated Value Format was designed to preserve Excel type data. 

BADC-CSV format is given by the [new_ASCII_file_format_guide.md](./docs/BADC_text_file_guide.md) and also by the [badc-csv-format.pdf](./docs/badc-csv-format.pdf)


## Core Functionality

This tool will evaluate a CSV file against the BADC-CSV standard as given.

The tool provides a level of compliance - corresponding to the 5 set out by the standard. CSV, Structure, Valid Metadata, Basic, and Complete. Then give a set of Errors that must be addressed to reach the next level. As each level in the standard requires the previous. Then a set of Warnings found at that level and all previous levels.

This report is given in free-text or JSON format.

Examples
```
uv run python -m badc_csv tests/reference/test2.csv --json
uv run python -m badc_csv tests/reference/additional/ukmo-metdb_lndsyn_20240202.csv --json
```



### Other tools

You can make BADC-CSV compliant headers using the tool provided by the following form, written by Molly Macrae.

https://github.com/mollymacrae/BADC-CSV-form
