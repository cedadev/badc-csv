from badc_csv.compliance.metadata import Metadata

from .cdl_template import CDL_Templates


def write_template(metadata: Metadata, data: dict):  # TODO
    """Take a representation and produce the CDL text.

    Create the requisite parts and fill the template.
    """
    TEMP = "TEMP"

    def write_global_attribute_text(global_attributes):
        all_global_attribute_lines = []
        for attribute, lines in global_attributes.items():
            all_global_attribute_lines.append(
                CDL_Templates.GLOBAL_ATTRIBUTE_LINE_TEMPLATE.format(
                    attribute=attribute, value=",".join(lines[0])
                )
            )
            if len(lines) > 1:
                # Unclear how to handle multi-line attributes when converting to NetCDF/CDL.
                # Due to how permissive the BADC-CSV standard is.
                # Deciding to create additional headings, which are numbered.
                for i, line in enumerate(lines[1:], start=2):
                    all_global_attribute_lines.append(
                        CDL_Templates.GLOBAL_ATTRIBUTE_LINE_TEMPLATE.format(
                            attribute=f"{attribute}{i}", value=",".join(line)
                        )
                    )
        return "\n".join(all_global_attribute_lines)

    global_attribute_text = write_global_attribute_text(
        metadata.get_global_attributes()
    )

    cdl_file: str = CDL_Templates.CDL_TEMPLATE_ONE_DIMENSION.format(
        filename=TEMP,
        dimensions_size_declarations_inc_tabs=TEMP,
        all_variables_lines_inc_tabs=TEMP,
        all_global_attribute_lines_inc_tabs=global_attribute_text,
        all_data=TEMP,
    )

    print(cdl_file)

    return cdl_file


# def test_conversion():
#     metadata, data = read_data(
#         "tests/reference/additional/midas-open_uk-hourly-rain-obs_dv-202007_dumfriesshire_01023_eskdalemuir_qcv-1_2018.csv"
#     )
#     write_template(*out)
