#! /usr/bin/env python3

import tempfile
import shutil
from pathlib import Path
import datetime
import pytz
from typing import List


def exclude_day(days_to_exclude: List, checkdatetime):
    """
    days_to_exclude format example; '["2020-08-09:2020-08-30", "2020-09-02:2020-09-05"]'
    """
    for period in days_to_exclude:
        start, end = period.split(":")  # start, end =
        # map(datetime.datetime.strptime("2015-01-30", "%Y-%m-%d"))
        start = datetime.datetime.strptime(start, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
        end = datetime.datetime.strptime(end, "%Y-%m-%d").replace(tzinfo=pytz.UTC)

        # let's make it the end of the day
        end = end.replace(hour=23, minute=59, second=59, microsecond=999999)


        if checkdatetime >= start and checkdatetime <= end:
            return True
    return False


def test_exclude_day():
    range1 = ["2020-08-09:2020-08-30", "2020-09-02:2020-09-05"]

    # not excluded
    a_dt = datetime.datetime(1944, 6, 4, tzinfo=pytz.UTC)
    assert not exclude_day(range1, a_dt)
    a_dt = datetime.datetime(2020, 9, 1, tzinfo=pytz.UTC)
    assert not exclude_day(range1, a_dt)
    a_dt = datetime.datetime(2020, 9, 6, tzinfo=pytz.UTC)
    assert not exclude_day(range1, a_dt)
    a_dt = datetime.datetime(2020, 8, 8, hour=23, minute=59, second=59, microsecond=999999, tzinfo=pytz.UTC)
    assert not exclude_day(range1, a_dt)

    # excluded
    a_dt = datetime.datetime(2020, 8, 30, hour=23, minute=59, second=59, microsecond=999999, tzinfo=pytz.UTC)
    assert exclude_day(range1, a_dt)
    a_dt = datetime.datetime(2020, 8, 9, tzinfo=pytz.UTC)
    assert exclude_day(range1, a_dt)

    range2 = ["2020-08-09:2020-08-09"]
    # excluded
    a_dt = datetime.datetime(2020, 8, 9, hour=23, minute=59, second=59, microsecond=999999, tzinfo=pytz.UTC)
    assert exclude_day(range1, a_dt)
    a_dt = datetime.datetime(2020, 8, 9, tzinfo=pytz.UTC)
    assert exclude_day(range1, a_dt)