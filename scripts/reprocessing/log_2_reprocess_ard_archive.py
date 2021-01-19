#!/usr/bin/env python3

"""

Step 1 – duplicate dataset to be archived in staging area

1.       Duplicate the [to be] archived dataset in “staging for removal” location”

2.       Update location [in ODC] to point to location in “staged for removal location”

3.       Wait prerequisite flush period (until queue empties)

4.       Trash original

Step 2 – write new replacement dataset

1.       Produce new dataset

2a.       Index new dataset
2b.       Archive the staged for deletion original dataset.

3.       Trash staged for removal copy.

Requirements
1.1 Needs the new location and a list of all the old ARD directories to move to the new location.
1.2 the uuids of the old _ard datasets to move and a way of knowing the new dir location
1.4 Needs a list of directories to move to a trash area, and then delete

2.1 needs a list of reprocessed ls8 l1 tars to ard process
2.1b needs a go scene script to do the processing 
2.2b Needs a list of old ard scenes to archive
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
    """Return None or a dictionary with key chopped_scene_id, uri and id.
"""

    processed_ard_scene_ids = {}
    for result in dc.index.datasets.search_returning(
            ("landsat_scene_id", "id", "uri"), product=product):
        choppped_id = chopped_scene_id(result.landsat_scene_id)
        if choppped_id in processed_ard_scene_ids:
            # The same chopped scene id has multiple scenes
            print ("The same chopped scene id has multiple scenes")
            #old_uuid = processed_ard_scene_ids[choppped_id]["id"]
            #LOGGER.warning(MANYSCENES, SCENEID=result.landsat_scene_id, old_uuid=old_uuid, new_uuid=result.id)

        processed_ard_scene_ids[chopped_scene_id(result.landsat_scene_id)] = {
            "uri": result.uri,
            "id": result.id,
        } # The uri gets the yaml.  I want the tar
    return processed_ard_scene_ids

dc = datacube.Datacube(app="gen-list")
product='ga_ls8c_ard_3'
print(dc.index.datasets.get_field_names(product_name=product))
processed_ard_scene_ids = calc_processed_ard_scene_ids(dc, product)
chopped_landsat_scene_ids = []
new_l1 = {}
blocked_scenes = 0
with open(log_file) as f:
    for line in f:
        line_dict = json.loads(line)
        #print (line_dict)
        if 'reason' in line_dict and line_dict['reason'] == "Potential reprocessed scene blocked from ARD processing":
            blocked_scenes += 1
            print (line_dict)
            chopped_scene = chopped_scene_id(line_dict['landsat_scene_id'])
            chopped_landsat_scene_ids.append(chopped_scene)
            new_l1[chopped_scene] = line_dict['dataset_path']
            
print (blocked_scenes)
print (chopped_landsat_scene_ids)

# The old way
# let's build a dictionary that has all the info.
old_ard_uuids = []
grouped_data = {}
for chopped_landsat_scene_id in chopped_landsat_scene_ids:
    if chopped_landsat_scene_id in processed_ard_scene_ids:
        print (processed_ard_scene_ids[chopped_landsat_scene_id])
        old_ard_uuids.append(processed_ard_scene_ids[chopped_landsat_scene_id]['id'])
        grouped_data[chopped_landsat_scene_id] = {
            "l1_new_dataset_path":None,
            "ard_old_dataset_dir":None,
            "ard_old_dataset_dir":None,
            
        }

# The new way
# Building a dict with all the info.
        
# l1_new_dataset_path - R2.1 Needed for the list of tars to ARD process
# "ard_old_dataset_yaml - used for moving out of the way
# ard_old_uuid - R2.2b updating and archiving

grouped_data = {}
for chopped_scene, l1_ard_path in new_l1.items():
    if chopped_scene in processed_ard_scene_ids:
        #dc.index.datasets.search(landsat_scene_id=landsat_scene_id, product=product)
        ard_old_uuid = processed_ard_scene_ids[chopped_scene]['id']
        a_dataset_list = list(dc.index.datasets.search(id=ard_old_uuid, product=product))
        assert len(a_dataset_list) == 1
        a_dataset = a_dataset_list[0]
        #print(a_dataset)
        #print(dir(a_dataset))
        #print(a_dataset.local_path)

        #print (list(a_dataset))
        #print (a_dataset[0].metadata.landsat_product_id)
        # Unknown field 'landsat_product_id'.
        #file_path = (dataset.local_path.parent.joinpath(dataset.metadata.landsat_product_id).with_suffix(".tar").as_posix())
        grouped_data[chopped_scene] = {
            "l1_new_dataset_path":l1_ard_path,
            "ard_old_dataset_yaml":a_dataset.local_path,
            "ard_old_uuid":str(ard_old_uuid),
            
        }

if False:
    print ('******** new_l1  **********')
    print (new_l1)
    print ('******************')

   
if True:        
    print ('******** grouped_data  **********')
    print (grouped_data)
    print ('******************')

            
if False: #True:
    f_out = open("old_ards_to_archive.txt", "w")
    for a_uuid in old_ard_uuids:
        f_out.write(str(a_uuid) + '\n')
    f_out.close()

if True:
    f_out = open("old_ards_to_archive.txt", "w")
    for a_uuid in old_ard_uuids:
        f_out.write(str(a_uuid) + '\n')
    f_out.close()


# for requirement 2.2b
if False:
        # this produced empty data sets
        datasets =  list(dc.index.datasets.search(landsat_scene_id=landsat_scene_id, product=product))
        # There should only be 1 dataset per scene
        #assert len(datasets) == 1
        print ('*****************')
        print (len(datasets))
        print (list(datasets))       
