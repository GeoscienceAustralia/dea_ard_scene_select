#! /usr/bin/env python3

import tempfile
import shutil
from pathlib import Path

from scene_select.ard_scene_select import scene_select, DATA_DIR
from scene_select.generate_aoi import generate_region
from scene_select.check_ancillary import BRDF_DIR, WV_DIR

OZWRS = DATA_DIR.joinpath("Australian_Wrs_list.txt")
TEST_DATA_DIR = Path(__file__).parent.joinpath("test_data")
STANDARD_SCENES_SELECTED = TEST_DATA_DIR.joinpath("standard_scenes_to_ARD_process.txt")
L1EXAMPLES = TEST_DATA_DIR.joinpath("All_Landsat_Level1_Nci_Files.txt")
# The Worldwide Reference System (WRS) is a global notation system for Landsat data.
STANDARD_WRS_AOI = TEST_DATA_DIR.joinpath("standard_wrs_list.txt")
STANDARD_MGRS_AOI = TEST_DATA_DIR.joinpath("australian_mgrs_aoi.txt")
# actually, we done have the results file yet...


def test_generate_aoi_main():

    dirpath = tempfile.mkdtemp()
    _, allowed_codes = generate_region.callback(satellite_data_provider="USGS", workdir=dirpath)
    standard = set(line.strip() for line in open(STANDARD_WRS_AOI))
    results = set(allowed_codes)

    # Note this is just comparing the results from the past to when you ran the test
    # Good for stopping new errors coming in
    # Will not pick up anything bad before then
    assert standard == results

    # remove the dirpath
    shutil.rmtree(dirpath)

    
def test_generate_mgrs_aoi():

    dirpath = tempfile.mkdtemp()
    _, allowed_codes = generate_region.callback(satellite_data_provider="ESA", workdir=dirpath)
    standard = set(line.strip() for line in open(STANDARD_MGRS_AOI))
    results = set(allowed_codes)

    # Note this is just comparing the results from the past to when you ran the test
    # Good for stopping new errors coming in
    # Will not pick up anything bad before then
    assert standard == results
    print (dirpath)

    # delete dirpath
    shutil.rmtree(dirpath)
