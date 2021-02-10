#!/usr/bin/env python3

"""

"""
import pathlib
import json
import jsonpickle

import re
import datacube

in_file = "in_area_19shr_chopped_scene_id.txt"


L8_PATTERN = (
    r"^(?P<sensor>LC)"
    r"(?P<satellite>08)_"
    r"(?P<processingCorrectionLevel>L1TP|L1GT)_"
    r"(?P<wrsPath>[0-9]{3})"
    r"(?P<wrsRow>[0-9]{3})_"
    r"(?P<acquisitionDate>[0-9]{8})_"
    r"(?P<processingDate>[0-9]{8})_"
    r"(?P<collectionNumber>01)_"
    r"(?P<collectionCategory>T1|T2)"
    r"(?P<extension>)$"
)


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


def calc_processed_ard_scene_ids(dc, product):
    """Return None or a dictionary where key ischopped_scene_id, 
    value is uri and id in a dictionary.
"""

    processed_ard_scene_ids = {}
    for result in dc.index.datasets.search(product=product):
        choppped_id = chopped_scene_id(result.metadata.landsat_scene_id)
        if choppped_id in processed_ard_scene_ids:
            # The same chopped scene id has multiple scenes
            print("The same chopped scene id has multiple scenes")

        processed_ard_scene_ids[choppped_id] = {
            "uri": result.local_path,
            "id": result.id,
            "product_id": result.metadata.landsat_product_id,
        }  # The uri gets the yaml.  I want the tar
    return processed_ard_scene_ids


# Can I get a product_id? Yeah

dc = datacube.Datacube(app="gen-list")
product = "ga_ls8c_ard_3"
product = "usgs_ls8c_level1_1"

# print(dc.index.datasets.get_field_names(product_name=product))

processed_ard_scene_ids = calc_processed_ard_scene_ids(dc, product)
chopped_landsat_scene_ids = []
new_l1 = {}
blocked_scenes = 0

# print (processed_ard_scene_ids)

with open(in_file) as f:
    for a_chopped_scene_id in f:
        a_chopped_scene_id = a_chopped_scene_id.strip()
        if a_chopped_scene_id in processed_ard_scene_ids:
            scene = processed_ard_scene_ids[a_chopped_scene_id]
            print("yeah")
            print(scene["product_id"])
            matchObj = re.match(L8_PATTERN, scene["product_id"])
            the_pd = matchObj.group("processingDate")
            if not (the_pd == "20201023" or the_pd == "20201022"):
                print("Strange processing Date: " + the_pd)
        else:
            print("nah")
            print(a_chopped_scene_id)

if False:  # True:
    f_uuid = open("old_ards_to_archive.txt", "w")
    f_old_ard_yaml = open("old_ard_yaml.txt", "w")
    for _, scene in grouped_data.items():
        print(scene)
        base = "/g/data/xu18/ga/"
        print(type(scene["ard_old_dataset_yaml"]))
        print(scene["ard_old_dataset_yaml"].parts)
        print(scene["ard_old_dataset_yaml"].relative_to(base))
        path_from_base = scene["ard_old_dataset_yaml"].relative_to(base)
        f_old_ard_yaml.write(str(path_from_base) + "\n")
    f_uuid.close()
    f_old_ard_yaml.close()


if False:
    # This isn't being used by anything.
    # It's more a record.
    with open("grouped_data.jsonpickle", "w") as handle:
        # TypeError: Object of type 'PosixPath' is not JSON serializable
        # json.dump(grouped_data, handle)
        json_obj = jsonpickle.encode(grouped_data)
        handle.write(json_obj)
        # jsonpickle.dump(grouped_data, handle)
