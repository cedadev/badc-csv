from badc_csv.format_checker import ComplianceChecker
from tests.util import TEST_DATA_DIR

DEBUG = False


def test_read_bad_data_heading():
    # Read an otherwise sound file with a "Data" instead of "data" heading.
    file = "test1.csv"
    checker = ComplianceChecker()
    # checker.set_verbose(True)
    compliance_level, errors = checker.compliance_assessment(
        TEST_DATA_DIR / file
    )
    if DEBUG:
        print(compliance_level)
        print(errors)
    assert compliance_level == ComplianceChecker.COMPLIANCE_LEVEL.CSV
    assert len(errors) >= 2


def test_read_compliant():
    # Read a sound
    file = "test2.csv"
    checker = ComplianceChecker()
    # checker.set_verbose(True)
    compliance_level, errors = checker.compliance_assessment(
        TEST_DATA_DIR / file
    )
    if DEBUG:
        print(compliance_level)
        print(errors)
    assert compliance_level == ComplianceChecker.COMPLIANCE_LEVEL.VALID_METADATA
    assert len(errors) > 0


def test_read_long():
    # Read a sound
    file = "badc-csv-multiline.csv"
    checker = ComplianceChecker()
    # checker.set_verbose(True)
    compliance_level, errors = checker.compliance_assessment(
        TEST_DATA_DIR / file
    )
    if DEBUG:
        print(compliance_level)
        print(errors)
    assert compliance_level == ComplianceChecker.COMPLIANCE_LEVEL.VALID_METADATA
    assert len(errors) > 0
