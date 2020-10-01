#! /usr/bin/env python3

import tempfile
import shutil
from pathlib import Path
import datetime
import pytz
from typing import List

def test_exclude_day():
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