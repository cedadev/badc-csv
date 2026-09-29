from badc_csv.format_checker import ComplianceChecker
from tests.util import TEST_DATA_DIR

DEBUG = True


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
        print(errors.get_warnings())
    # file has no 'coordinate_variable'
    assert compliance_level == ComplianceChecker.COMPLIANCE_LEVEL.COMPLETE
    assert len(errors) == 0
    assert errors.num_warnings() > 0  # 'coordinate_variable'


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
        print(errors.get_warnings())
    # file has no 'coordinate_variable'
    assert compliance_level == ComplianceChecker.COMPLIANCE_LEVEL.COMPLETE
    assert len(errors) == 0
    assert errors.num_warnings() > 0  # 'coordinate_variable'


def test_read_additional():
    file = "additional/ukmo-metdb_lndsyn_20240202.csv"
    checker = ComplianceChecker()
    # checker.set_verbose(True)
    compliance_level, errors = checker.compliance_assessment(
        TEST_DATA_DIR / file
    )
    if DEBUG:
        print(compliance_level)
        print(errors)
        print(errors.get_warnings())
    assert compliance_level == ComplianceChecker.COMPLIANCE_LEVEL.STRUCTURE
    assert len(errors) >= 2  # reference G, standard_name 137,
    assert errors.num_warnings() > 0  # Comments...


def test_read_additional_amended():
    file = "amended/ukmo-metdb_lndsyn_20240202.csv"
    checker = ComplianceChecker()
    # checker.set_verbose(True)
    compliance_level, errors = checker.compliance_assessment(
        TEST_DATA_DIR / file
    )
    if DEBUG:
        print(compliance_level)
        print(errors)
        print(errors.get_warnings())
    assert compliance_level == ComplianceChecker.COMPLIANCE_LEVEL.VALID_METADATA
    assert len(errors) >= 0
    assert errors.num_warnings() > 0  # Comments..., 'coordinate_variable'
