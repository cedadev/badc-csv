import warnings
from pathlib import Path

from badc_csv.badc_errors import BADCTextFileError
from badc_csv.badctextfilewarn import BADCTextFile

TEST_DATA_DIR = Path("tests/reference/")
TEST_TEMP_DIR = Path("tests/tmp/")


def read_file_text(filepath):
    with open(filepath, "r") as f:
        return f.read()


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



def test_read_bad():
    with open(TEST_DATA_DIR / "badc-csv-unsupported-multiline.csv", "r") as fh:
        # this file uses an unsupported format of multi-line comments
        try:
            BADCTextFile(fh)
            assert False
        except BADCTextFileError:
            assert True



def test_expect_warnings():
    ...
    # Example where we expect 7 warnings
    # with pytest.warns() as record_complete:
    #     t.check_complete("complete")
    # assert len(record_complete) == 7


def test_cdl_maybe_(): # unsure...
    ...
    # with open(r".tmp/test1.cdl", "wb") as fh:
    #     fh.write(t.cdl().encode("utf-8"))
    #     fh.close()
    #     print(t.cvs())

    # t.check_complete(1)
    # with open(r".tmp/test1.cdl", "wb") as fh2:
    #     fh2.write(t.cdl().encode("utf-8"))