class BADCTextFileError(Exception):
    pass


class BADCTextFileParseError(BADCTextFileError):
    pass  # basic conform to format


class BADCTextFileDataError(BADCTextFileError):
    pass  # wrong shape data


class BADCTextFileMetadataInvalid(BADCTextFileError):
    pass  # wrong args for md


class BADCTextFileMetadataIncomplete(BADCTextFileError):
    pass  # mandatory fields not included


class BADCTextFileMetadataNonstandard(BADCTextFileError):
    pass  # values not in std lists
