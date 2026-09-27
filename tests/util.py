from pathlib import Path

TEST_DATA_DIR = Path("tests/reference/")
TEST_TEMP_DIR = Path("tests/tmp/")


def read_file_text(filepath):
    with open(filepath, "r") as f:
        return f.read()
