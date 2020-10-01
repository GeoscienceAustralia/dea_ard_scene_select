#! /usr/bin/env python3

import tempfile
import shutil
from pathlib import Path
import datetime
import pytz
from typing import List

def bad_day(days_to_exclude: List, checkdatetime):
    """
    days_to_exclude format example; '["2020-08-09:2020-08-30", "2020-09-02:2020-09-05"]'
    """
    for period in days_to_exclude:
        start, end = period.split(':') #start, end =
        #map(datetime.datetime.strptime("2015-01-30", "%Y-%m-%d"))
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
        print (start)
        print (end)

def test_bad_day():
    a_dt = datetime.datetime(1944, 6, 4, tzinfo=pytz.UTC)
    bad_day(["2020-08-09:2020-08-30", "2020-09-02:2020-09-05"], a_dt)
