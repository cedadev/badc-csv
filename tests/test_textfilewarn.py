import warnings

from badc_csv.checker_warning.badctextfilewarn import BADCTextFile
from tests.util import TEST_DATA_DIR, TEST_TEMP_DIR, read_file_text


def test_initial():
    # TEST 1: Create a 'BADC-CSV' file
    ground_truth = read_file_text(TEST_DATA_DIR / "bigshot-example.csv")
    with open(TEST_TEMP_DIR / "xxx.csv", "w+") as fh:
        t = BADCTextFile(fh)
        d1 = (1.2, 3.4, 5.6, 5.2)
        d2 = (2.2, 4.4, 5.7, 15.2)
        t.add_variable("temp", d1)
        t.add_variable("height", d2)
        t.add_metadata("units", "K", 1)
        t.add_metadata("Creator", "Sam Pepler")
        t.add_metadata("Creator", ("Prof Bigshot", "Reading uni"))
        bigshot_output = t.__repr__()

    assert ground_truth == bigshot_output


def test_read_compliant():
    # TEST 2: Read a 'BADC-CSV' compliant file
    ground_truth = read_file_text(TEST_DATA_DIR / "weather-example.csv")

    with open(TEST_DATA_DIR / "test1.csv", "r") as fh:
        t = BADCTextFile(fh)
        weather_example = t.__repr__()
        assert ground_truth == weather_example

        # Source - https://stackoverflow.com/a/45671804
        # Posted by zezollo, modified by community. See post 'Timeline' for change history
        # Retrieved 2026-09-21, License - CC BY-SA 4.0
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            # Error if ANY warnings created
            t.check_complete("basic")
            t.check_complete(0)
            t.check_complete("complete")
