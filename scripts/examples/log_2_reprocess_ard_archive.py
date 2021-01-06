#!/usr/bin/env python3

"""

"""

import json
import datacube

log_file = '/g/data1a/u46/users/dsg547/sandpit/dea-ard-scene-select/scripts/examples/scratch/find_blocked_usgs_ls8c_level1_1/ard_scene_select.log'

ARD_PARENT_PRODUCT_MAPPING = {
    "ga_ls5t_level1_3": "ga_ls5t_ard_3",
    "ga_ls7e_level1_3": "ga_ls7e_ard_3",
    "usgs_ls5t_level1_1": "ga_ls5t_ard_3",
    "usgs_ls7e_level1_1": "ga_ls7e_ard_3",
    "usgs_ls8c_level1_1": "ga_ls8c_ard_3",
}


def chopped_scene_id(scene_id: str) -> str:
    """
    Remove the groundstation/version information from a scene id.

    >>> chopped_scene_id('LE71800682013283ASA00')
    'LE71800682013283'
    """
    if len(scene_id) != 21:
        raise RuntimeError(f"Unsupported scene_id format: {scene_id!r}")
    capture_id = scene_id[:-5]
    return capture_id


def calc_processed_ard_scene_ids(dc, ard_product):
    """Return None or a dictionary with key chopped_scene_id and value  maturity level.
"""

    processed_ard_scene_ids = {}
    for result in dc.index.datasets.search_returning(
            ("landsat_scene_id", "dataset_maturity", "id"), product=product):
        choppped_id = chopped_scene_id(result.landsat_scene_id)
        if choppped_id in processed_ard_scene_ids:
            # The same chopped scene id has multiple scenes
            print ("The same chopped scene id has multiple scenes")
            #old_uuid = processed_ard_scene_ids[choppped_id]["id"]
            #LOGGER.warning(MANYSCENES, SCENEID=result.landsat_scene_id, old_uuid=old_uuid, new_uuid=result.id)

        processed_ard_scene_ids[chopped_scene_id(result.landsat_scene_id)] = {
            "dataset_maturity": result.dataset_maturity,
            "id": result.id,
        }
    return processed_ard_scene_ids

dc = datacube.Datacube(app="gen-list")
product='ga_ls8c_ard_3'

processed_ard_scene_ids = calc_processed_ard_scene_ids(dc, product)
landsat_scene_ids = []
sum = 0
with open(log_file) as f:
    for line in f:
        line_dict = json.loads(line)
        #print (line_dict)
        if 'reason' in line_dict and line_dict['reason'] == "Potential reprocessed scene blocked from ARD processing":
            sum += 1
            print (line_dict)
            landsat_scene_ids.append(chopped_scene_id(line_dict['landsat_scene_id']))

print (sum)
print (landsat_scene_ids)
for landsat_scene_id in landsat_scene_ids:
    if False:
        # this produced empty data sets
        datasets =  list(dc.index.datasets.search(landsat_scene_id=landsat_scene_id, product=product))
        # There should only be 1 dataset per scene
        #assert len(datasets) == 1
        print ('*****************')
        print (len(datasets))
        print (list(datasets))
    if landsat_scene_id in processed_ard_scene_ids:
        print (processed_ard_scene_ids[landsat_scene_id])

if False:
    f_out = open("my_to_archive.txt", "w")
    for a_uuid in uuids:
        f_out.write(a_uuid + '\n')
        f_out.close() 
