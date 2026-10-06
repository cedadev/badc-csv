from pathlib import Path

# Let the user deal with reading/writing files...


def netcdf_to_badc():
    # TODO issue-#8
    ...


def badc_to_netcdf(src: str, dest: Path) -> bool:
    # TODO issue-#7

    """
    src str: is the text of a badc-csv file.
        This file is assumed to have COMPLETE compliance to the standard.

    returns bool: if it was successful converting and writing the NETCDF file.

    """

    # https://docs.xarray.dev/en/stable/user-guide/io.html
    # https://docs.xarray.dev/en/stable/generated/xarray.Dataset.to_netcdf.html#xarray.Dataset.to_netcdf
    # xarray.Dataset
    # xarray.Dataset.to_netcdf


def badc_to_cdl():
    """CDL (Common Data Language) is a format that corresponds to NetCDF.

    CDL is the output and input format of ncdump and ncgen respectively,
        ncdump and ncgen being two key NetCDF command line utilities

    This is necessary as NetCDF is a BINARY format, optimized for access and computation
    -- meaning that a text editor cannot natively read it
    """
