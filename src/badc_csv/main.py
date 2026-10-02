import argparse
import json
from pathlib import Path

from badc_csv.format_checker import ComplianceChecker
from badc_csv.util.error_collection import ErrorCollection


def create_report_json(
    file: Path,
    compliance_level: ComplianceChecker.COMPLIANCE_LEVEL,
    errors: ErrorCollection,
) -> str:
    return json.dumps(
        {
            "file": str(file),
            "compliance_level": compliance_level.name,
            "errors": [e for e in errors.get_errors()],
            "warnings": [w for w in errors.get_warnings()],
        },
        indent=4,
    )


def create_report_text(
    file: Path,
    compliance_level: ComplianceChecker.COMPLIANCE_LEVEL,
    errors: ErrorCollection,
) -> str:
    title_card = f"File {file} has a Compliance Level: {compliance_level}\n"

    error_text = "Errors Given:\n" + (
        "\n".join(f"Error: {e}" for e in errors.get_errors())
        if errors.num_errors() > 0
        else "No errors given."
    )

    warning_text = "Warnings Given:\n" + (
        "\n".join(f"Warning: {w}" for w in errors.get_warnings())
        if errors.num_warnings() > 0
        else "No warnings given."
    )

    return title_card + error_text + "\n" + warning_text + "\n"


def main(
    filename: Path, verbose: bool, disallow_warnings: bool, json: bool = False
) -> str:
    """
    filename: -f or positional. type: path - REQUIRED - file being validated.
    verbose: -v. type: flag - display additional information during processing
    disallow-warnings: -w --disallow-warnings. type: flag - treat warnings as errors
    json-format: --json. type: flag - provide output in JSON format, not free text.
    """
    checker = ComplianceChecker()
    checker.set_verbose(verbose)
    checker.disallow_warnings(disallow_warnings)
    compliance_level, errors = checker.compliance_assessment(filename)

    if json:
        return create_report_json(filename, compliance_level, errors)
    else:
        return create_report_text(filename, compliance_level, errors)


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
    p.add_argument(
        "--json", action="store_true", help="return output in JSON format"
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
    print(args.filename, args.verbose, args.disallow_warnings, args.json)
    report = main(
        args.filename, args.verbose, args.disallow_warnings, args.json
    )
    print(report)


"""
Examples for use.
```
uv run python src/badc_csv/main.py -f tests/reference/test2.csv
uv run python src/badc_csv/main.py -f tests/reference/test2.csv --json
uv run python src/badc_csv/main.py -f tests/reference/test2.csv --json -v
uv run python src/badc_csv/main.py -f tests/reference/additional/ukmo-metdb_lndsyn_20240202.csv --json
uv run python src/badc_csv/main.py -f tests/reference/additional/ukmo-metdb_lndsyn_20240202.csv --json -w
uv run python src/badc_csv/main.py -f tests/reference/amended/ukmo-metdb_lndsyn_20240202.csv --json
uv run python src/badc_csv/main.py -f tests/reference/amended/ukmo-metdb_lndsyn_20240202.csv --json -w
uv run python src/badc_csv/main.py tests/reference/additional/midas-open_uk-hourly-rain-obs_dv-202007_dumfriesshire_01023_eskdalemuir_qcv-1_2018.csv --json
```
"""
