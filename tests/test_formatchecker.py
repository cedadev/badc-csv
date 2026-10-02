from badc_csv.format_checker import ComplianceChecker
from tests.util import standard_test

COMPLIANCE_LEVEL = ComplianceChecker.COMPLIANCE_LEVEL

DEBUG = False


def test_read_bad_data_heading():
    # Incorrect headings "Data" instead of "data" heading.
    standard_test(
        rel_filepath="test1.csv",
        expected_level=COMPLIANCE_LEVEL.CSV,
        num_errors=2,
        errors_comparison_type="eq",
        num_warnings=0,
        verbose=False,
        debug=DEBUG,
    )


def test_read_compliant():
    # compliant file, but with warnings for no 'coordinate_variable'
    standard_test(
        rel_filepath="test2.csv",
        expected_level=COMPLIANCE_LEVEL.COMPLETE,
        num_errors=0,
        # file has no 'coordinate_variable'
        num_warnings=1,
        warnings_comparison_type="gte",
        debug=DEBUG,
    )


def test_read_compliant_block_warnings():
    # compliant file, but with warnings for no 'coordinate_variable'
    # this time... treat warnings as errors. Lowers file to "VALID METADATA".
    standard_test(
        rel_filepath="test2.csv",
        expected_level=COMPLIANCE_LEVEL.VALID_METADATA,
        num_errors=0,
        # file has no 'coordinate_variable'
        num_warnings=1,
        warnings_comparison_type="gte",
        debug=DEBUG,
        disallow_warnings=True,  # but treat warnings as errors
    )


def test_read_long_compliant():
    # compliant file, but with warnings for no 'coordinate_variable'
    standard_test(
        rel_filepath="badc-csv-multiline.csv",
        expected_level=COMPLIANCE_LEVEL.COMPLETE,
        num_errors=0,
        # file has no 'coordinate_variable'
        num_warnings=1,
        warnings_comparison_type="gte",
        debug=DEBUG,
    )


def test_read_ukmo():
    # In-use file. UKMO-METDB dataset.
    # Error Valid Metadata: 'reference' too many columns, 'standard_name' col 137 is incorrect,
    # Warning: Non-compliant use of comments.
    standard_test(
        rel_filepath="additional/ukmo-metdb_lndsyn_20240202.csv",
        expected_level=COMPLIANCE_LEVEL.STRUCTURE,
        num_errors=2,
        # file has no 'coordinate_variable'
        num_warnings=1,
        warnings_comparison_type="gte",
        debug=DEBUG,
    )


def test_read_additional_amended():
    # In-use file. UKMO-METDB dataset.
    # With some amendments, it can be made more compliant!
    # Error COMPLIANT however: no 'type' attribute for various columns
    # Warning: Non-compliant use of comments, file has no 'coordinate_variable'
    standard_test(
        rel_filepath="amended/ukmo-metdb_lndsyn_20240202.csv",
        expected_level=COMPLIANCE_LEVEL.BASIC,
        num_errors=5,
        errors_comparison_type="gte",
        num_warnings=10,  # many repeated warnings
        warnings_comparison_type="gte",
        debug=DEBUG,
        verbose=True,
    )


def test_read_additional_midas():
    # In-use file. Midas Hourly Rain.
    # Completely compliant file.
    # COMPLETE, no errors, no warnings.
    standard_test(
        rel_filepath="additional/midas-open_uk-hourly-rain-obs_dv-202007_dumfriesshire_01023_eskdalemuir_qcv-1_2018.csv",
        expected_level=COMPLIANCE_LEVEL.COMPLETE,
        num_errors=0,
        debug=DEBUG,
    )
