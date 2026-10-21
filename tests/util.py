from pathlib import Path

from badc_csv.format_checker import ComplianceChecker

TEST_DATA_DIR = Path("tests/reference/")
TEST_TEMP_DIR = Path("tests/tmp/")


def read_file_text(filepath):
    with open(filepath, "r") as f:
        return f.read()


def __compare(a, b, method: str):
    comparison_types = ("gt", "eq", "lt", "gte", "lte")
    if method not in comparison_types:
        raise TypeError(
            f"Invalid comparison {method}, must be one of {comparison_types}."
        )
    if method == "gt":
        return a > b
    elif method == "gte":
        return a >= b
    elif method == "eq":
        return a == b
    elif method == "lt":
        return a < b
    elif method == "lte":
        return a <= b


def standard_test(
    rel_filepath: Path,
    expected_level: ComplianceChecker.COMPLIANCE_LEVEL,
    num_errors: int,
    errors_comparison_type: str = "eq",
    num_warnings: int = 0,
    warnings_comparison_type: str = "eq",
    verbose: bool = False,
    debug: bool = False,
    disallow_warnings: bool = False,
):
    checker = ComplianceChecker()
    checker.set_verbose(verbose)
    checker.disallow_warnings(disallow_warnings)
    compliance_level, errors = checker.compliance_assessment(
        TEST_DATA_DIR / rel_filepath
    )
    if debug:
        print(compliance_level)
        print(errors.num_errors(), errors.get_errors())
        print(errors.num_warnings(), errors.get_warnings())
    assert compliance_level == expected_level
    assert __compare(len(errors), num_errors, errors_comparison_type)
    assert __compare(
        errors.num_warnings(), num_warnings, warnings_comparison_type
    )
