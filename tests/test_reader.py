from badc_csv.compliance.reader import reader

# As per `test_formatchecker.py`, this file passes validation to level COMPLETE
test_metadata, test_data = reader(
    "tests/reference/additional/midas-open_uk-hourly-rain-obs_dv-202007_dumfriesshire_01023_eskdalemuir_qcv-1_2018.csv"
)


def test_dimensions():
    # Size of data, metadata is correct
    assert test_data.size == 5
    assert test_metadata.column_size() == 15

    # Every column requries a type
    cols = test_metadata.get_columns()
    for column in cols:
        assert test_metadata.get_column_type(column) is not None


def test_missing_and_fill_value():
    # This may change with the spec.
    assert "missing_value" in test_metadata.get_global_attributes()
