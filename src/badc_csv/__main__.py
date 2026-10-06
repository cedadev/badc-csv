import argparse
import json
from pathlib import Path

from badc_csv.format_checker import ComplianceChecker
from badc_csv.util.error_collection import ErrorCollection

type JsonText = str  # additional type hints


def create_report_json(
    file: Path,
    compliance_level: ComplianceChecker.COMPLIANCE_LEVEL,
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
    """
    filename: -f or positional. type: path - REQUIRED - file being validated.
    verbose: -v. type: flag - display additional information during processing
    disallow-warnings: -w --disallow-warnings. type: flag - treat warnings as errors
    """
    checker = ComplianceChecker()
    checker.set_verbose(verbose)
    checker.disallow_warnings(disallow_warnings)
    compliance_level, errors = checker.compliance_assessment(filename)

    return create_report_json(filename, compliance_level, errors)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    p = argparse.ArgumentParser(
        prog="BADC-CSV validation tool",
        description="Validate a BADC CSV file and report its compliance level, "
        "errors and warnings.",
    )
    p.add_argument(
        "filename_pos",
        nargs="?",
        type=Path,
        metavar="FILE",
        help="path to the file to validate (alternative to -f)",
    )
    p.add_argument(
        "-f",
        "--filename",
        dest="filename_opt",
        type=Path,
        metavar="FILE",
        help="path to the file to validate",
    )
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
    report = main(args.filename, args.verbose, args.disallow_warnings)
    print(report)


"""
Examples for use.
```
uv run python -m badc_csv tests/reference/test2.csv
uv run python -m badc_csv tests/reference/test2.csv
uv run python -m badc_csv -f tests/reference/test2.csv 
uv run python -m badc_csv tests/reference/test2.csv -v
uv run python -m badc_csv tests/reference/additional/ukmo-metdb_lndsyn_20240202.csv
uv run python -m badc_csv tests/reference/additional/ukmo-metdb_lndsyn_20240202.csv -w
uv run python -m badc_csv tests/reference/amended/ukmo-metdb_lndsyn_20240202.csv
uv run python -m badc_csv tests/reference/amended/ukmo-metdb_lndsyn_20240202.csv -w
uv run python -m badc_csv tests/reference/additional/midas-open_uk-hourly-rain-obs_dv-202007_dumfriesshire_01023_eskdalemuir_qcv-1_2018.csv
```
"""
