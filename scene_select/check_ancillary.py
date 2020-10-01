#!/usr/bin/env python3

import datetime
from pathlib import Path
import structlog
from functools import lru_cache

# This is needed when testing locally
# import hdf5plugin
import h5py
import numpy
import pandas


LOG = structlog.get_logger()
BRDF_DEFINITIVE_START_DATE = datetime.datetime(2002, 7, 1)
BRDF_DIR = "/g/data/v10/eoancillarydata-2/BRDF/MCD43A1.006"
WV_DIR = "/g/data/v10/eoancillarydata-2/water_vapour"
WV_FMT = "pr_wtr.eatm.{year}.h5"


def read_h5_table(fid, dataset_name):
    """
    From Wagl. Read a HDF5 `TABLE` as a `pandas.DataFrame`.

    :param fid:
        A h5py `Group` or `File` object from which to read the
        dataset from.

    :param dataset_name:
        A `str` containing the pathname of the dataset location.

    :return:
        Either a `pandas.DataFrame` (Default) or a NumPy structured
        array.
    """

    dset = fid[dataset_name]
    
    # grab the index names if we have them
    idx_names = dset.attrs.get("index_names")

    if dset.attrs.get("python_type") == "`Pandas.DataFrame`":
        col_names = dset.dtype.names
        dtypes = [dset.attrs["{}_dtype".format(name)] for name in col_names]
        dtype = numpy.dtype(list(zip(col_names, dtypes)))
        data = pandas.DataFrame.from_records(dset[:].astype(dtype), index=idx_names)
    else:
        data = pandas.DataFrame.from_records(dset[:], index=idx_names)
    return data


class AncillaryFiles:
    def __init__(self, brdf_dir=BRDF_DIR, water_vapour_dir=WV_DIR, wv_days_tolerance=1):
        self.brdf_path = Path(brdf_dir)
        self.wv_path = Path(water_vapour_dir)
        self.max_tolerance = -datetime.timedelta(days=wv_days_tolerance)

    @lru_cache(maxsize=32)
    def wv_file_exists(self, acquisition_year):
        wv_pathname = self.wv_path.joinpath(WV_FMT.format(year=acquisition_year))
        return wv_pathname.exists()

    @lru_cache(maxsize=32)
    def get_wv_index(self, acquisition_year):
        wv_pathname = self.wv_path.joinpath(WV_FMT.format(year=acquisition_year))
        with h5py.File(str(wv_pathname), "r") as fid:
            index = read_h5_table(fid, "INDEX")
        return index

    @lru_cache(maxsize=20000)
    def brdf_day_exists(self, ymd):
        brdf_day_of_interest = self.brdf_path.joinpath(ymd)
        return brdf_day_of_interest.exists()

    def definitive_ancillary_files(self, acquisition_datetime):

        if not self.wv_file_exists(acquisition_datetime.year):
            return False, "Water vapour data for year {} does not exist.".format(acquisition_datetime.year)

        # get year of acquisition to confirm definitive data
        index = self.get_wv_index(acquisition_datetime.year)

        # Removing timezone info since different UTC formats were clashing.
        acquisition_datetime = acquisition_datetime.replace(tzinfo=None)

        time_delta = index.timestamp - acquisition_datetime
        result = time_delta[(time_delta < datetime.timedelta()) & (time_delta > self.max_tolerance)]

        if result.shape[0] == 0:
            return False, "Water vapour data for {} does not exist.".format(acquisition_datetime)
        else:
            if acquisition_datetime < BRDF_DEFINITIVE_START_DATE:
                return True, ""
            else:
                ymd = acquisition_datetime.strftime("%Y.%m.%d")
                if self.brdf_day_exists(ymd):
                    return True, ""
                else:
                    return False, "BRDF data for {} does not exist.".format(ymd)


if __name__ == "__main__":
    pass
