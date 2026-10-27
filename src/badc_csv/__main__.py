import argparse
import json
from pathlib import Path

from badc_csv.compliance import COMPLIANCE_LEVEL, ComplianceChecker
from badc_csv.netcdf import transform_badccsv_to_netcdf
from badc_csv.util.error_collection import ErrorCollection

type JsonText = str  # additional type hints


def create_report_json(
    file: Path,
    compliance_level: COMPLIANCE_LEVEL,
    errors: ErrorCollection,
) -> JsonText:
    return json.dumps(
        {
            "file": str(file),
            "compliance_level": compliance_level.name,
            "errors": [e for e in errors.get_errors()],
            "warnings": [w for w in errors.get_warnings()],
        },
        indent=4,
    )


def main(filename: Path, verbose: bool, disallow_warnings: bool) -> JsonText:
    checker = ComplianceChecker()
    checker.set_verbose(verbose)
    checker.disallow_warnings(disallow_warnings)
    compliance_level, errors = checker.compliance_assessment(filename)
    return create_report_json(filename, compliance_level, errors)


def add_required_file(p):
    p.add_argument(
        "filename_pos",
        nargs="?",
        type=Path,
        metavar="FILE",
        help="INPUT File",
    )
    p.add_argument(
        "-f",
        "--filename",
        dest="filename_opt",
        type=Path,
        metavar="FILE",
        help="Path to the input file",
    )


def add_checker_parser(subparser):
    p = subparser.add_parser(
        "check",
        prog="BADC-CSV validation tool",
        description="Validate a BADC CSV file and report its compliance level, "
        "errors and warnings.",
    )
    add_required_file(p)
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="display additional information during processing",
    )
    p.add_argument(
        "-w",
        "--disallow-warnings",
        action="store_true",
        help="treat warnings as errors",
    )


def add_conversion_parser(subparser):
    p = subparser.add_parser(
        "transform",
        prog="Conversion tool for BADC-CSV",
        description="Converts a COMPLETE BADC-CSV file into a NetCDF4 file.",
    )
    add_required_file(p)
    p.add_argument(
        "-o",
        dest="output_file",
        required=True,
        type=Path,
        help="Result path for produced NetCDF file.",
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    p = argparse.ArgumentParser(prog="Utilities for the BADC_CSV file format.")
    subparsers = p.add_subparsers(dest="command", help="subcommand help")

    add_checker_parser(subparsers)
    add_conversion_parser(subparsers)
    return p


def parse_args() -> argparse.Namespace:
    p = build_parser()
    args = p.parse_args()

    if args.filename_pos and args.filename_opt:
        p.error("specify the file either positionally or with -f, not both")

    filename = args.filename_pos or args.filename_opt
    if filename is None:
        p.error("a file is required (positional or -f/--filename)")

    args.filename = filename
    return args


if __name__ == "__main__":
    args = parse_args()

    if args.command == "check":
        report = main(args.filename, args.verbose, args.disallow_warnings)
        print(report)

    elif args.command == "transform":
        transform_badccsv_to_netcdf(args.filename, args.output_file)


"""
Examples for use. 

Two subcommands, 1) check and 2) transform
```
uv run python -m badc_csv check tests/reference/test2.csv
uv run python -m badc_csv check tests/reference/test2.csv
uv run python -m badc_csv check -f tests/reference/test2.csv 
uv run python -m badc_csv check tests/reference/test2.csv -v
uv run python -m badc_csv check tests/reference/additional/ukmo-metdb_lndsyn_20240202.csv
uv run python -m badc_csv check tests/reference/additional/ukmo-metdb_lndsyn_20240202.csv -w
uv run python -m badc_csv check tests/reference/amended/ukmo-metdb_lndsyn_20240202.csv
uv run python -m badc_csv check tests/reference/amended/ukmo-metdb_lndsyn_20240202.csv -w
uv run python -m badc_csv check tests/reference/additional/midas-open_uk-hourly-rain-obs_dv-202007_dumfriesshire_01023_eskdalemuir_qcv-1_2018.csv
...
uv run python -m badc_csv transform <badc_csv_file> -o <destination_netcdf_file>
uv run python -m badc_csv transform tests/reference/additional/midas-open_uk-hourly-rain-obs_dv-202007_dumfriesshire_01023_eskdalemuir_qcv-1_2018.csv -o tests/tmp/test.nc
```
"""
