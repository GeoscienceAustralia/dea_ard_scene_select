#! /usr/bin/env python3

import tempfile
from pathlib import Path
import datetime
import pytz

from scene_select.ard_scene_select import dict2ard_arg_string, allowed_codes_to_region_codes, exclude_days


def test_dict2ard_arg_string():
    ard_click_params = {"index_datacube_env": "/g/data", "walltime": None}
    ard_arg_string = dict2ard_arg_string(ard_click_params)
    assert ard_arg_string == "--index-datacube-env /g/data"


def test_allowed_codes_to_region_codes():
    file_path = Path(tempfile.mkdtemp(prefix="testrun"), "config.yaml")
    with file_path.open(mode="w") as f:
        f.write("102_67\n")
        f.write("102_68\n")
    the_file_path = str(file_path)
    path_row_list = allowed_codes_to_region_codes(the_file_path)
    assert path_row_list == ["102067", "102068"]


def test_exclude_days():
    range1 = ["2020-08-09:2020-08-30", "2020-09-02:2020-09-05"]

    # not excluded
    a_dt = datetime.datetime(1944, 6, 4, tzinfo=pytz.UTC)
    assert not exclude_days(range1, a_dt)
    a_dt = datetime.datetime(2020, 9, 1, tzinfo=pytz.UTC)
    assert not exclude_days(range1, a_dt)
    a_dt = datetime.datetime(2020, 9, 6, tzinfo=pytz.UTC)
    assert not exclude_days(range1, a_dt)
    a_dt = datetime.datetime(2020, 8, 8, hour=23, minute=59, second=59, microsecond=999999, tzinfo=pytz.UTC)
    assert not exclude_days(range1, a_dt)

    # excluded
    a_dt = datetime.datetime(2020, 8, 30, hour=23, minute=59, second=59, microsecond=999999, tzinfo=pytz.UTC)
    assert exclude_days(range1, a_dt)
    a_dt = datetime.datetime(2020, 8, 9, tzinfo=pytz.UTC)
    assert exclude_days(range1, a_dt)

    range2 = ["2020-08-09:2020-08-09"]
    # excluded
    a_dt = datetime.datetime(2020, 8, 9, hour=23, minute=59, second=59, microsecond=999999, tzinfo=pytz.UTC)
    assert exclude_days(range1, a_dt)
    a_dt = datetime.datetime(2020, 8, 9, tzinfo=pytz.UTC)
    assert exclude_days(range1, a_dt)


def test_exclude_days_diff_tzinfo():
    range1 = ["2020-08-09:2020-08-30", "2020-09-02:2020-09-05"]

    # not excluded
    a_dt = datetime.datetime(1944, 6, 4, tzinfo=datetime.timezone.utc)
    assert not exclude_days(range1, a_dt)


def test_exclude_days_empty():
    range1 = []

    # not excluded
    a_dt = datetime.datetime(1944, 6, 4, tzinfo=datetime.timezone.utc)
    assert not exclude_days(range1, a_dt)
