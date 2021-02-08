#!/usr/bin/env python3

"""

Step 1 – duplicate ARD dataset to be archived in staging area

1.       Duplicate the [to be] archived ARD dataset in “staging for removal” location

2.       Update location [in ODC] to point to location in “staged for removal location

3.       Wait prerequisite flush period

4.       Trash original [ARD files that are in the old location, not referenced by the ODC anymore]

Step 2 – write new ARD replacement dataset

1.       Produce new dataset
2a.       Index new dataset
2b.       Archive the staged for deletion original dataset.

3.       Trash staged for removal copy.

Requirements
1.1 A list of all the old ARD directories to move to the new location, relative to the base dir. - produced by this code.
1.2 The base dir of the old location and the new location. 
1.4 No new requirements.

Do these steps by calling ard interface directly
2.1 needs a list of reprocessed ls8 l1 tars to ard process  
2.2b Needs a list of old ard uuid's to archive
"""
import pathlib
import json
import jsonpickle

import datacube


    
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


# It was this.  Why?
#def calc_processed_ard_scene_ids(dc, ard_product)

def calc_processed_ard_scene_ids(dc, product):
    """Return None or a dictionary where key ischopped_scene_id, 
    value is uri and id in a dictionary.
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

def files_out(grouped_data, uuid_file, old_ard_yaml_file, l1_new_dataset_file, base):
    """
    Write the files to be used by unix scripts to archive and reprocess.
    """
    f_uuid = open(uuid_file, "w")
    f_old_ard_yaml = open(old_ard_yaml_file, "w")
    f_l1_new_dataset_path = open(l1_new_dataset_file, "w")
    for _, scene  in grouped_data.items():
        #print(scene)
        #base = "/g/data/xu18/ga/" 
        path_from_base =  scene['ard_old_dataset_yaml'].relative_to(base)
        f_old_ard_yaml.write(str(path_from_base) + '\n')
        f_uuid.write(str(scene['ard_old_uuid']) + '\n')
        f_l1_new_dataset_path.write(str(scene['l1_new_dataset_path']) + '\n')
    f_uuid.close()
    f_old_ard_yaml.close()      

def write_dic(the_data, the_file):
    # This isn't being used by anything.
    # It's more a record.
    with open(the_file, 'w') as handle:
        # TypeError: Object of type 'PosixPath' is not JSON serializable
        # json.dump(grouped_data, handle)
        json_obj = jsonpickle.encode(the_data, indent=4)
        handle.write(json_obj)

        
def write_2_file(iterate_over, a_file):
    with open(a_file, 'w') as f:
        for item in iterate_over:
            f.write("%s" % item)

def generate_new_l1s(log_file, in_area_file):
    """
    Generate a dictionary, key is chopped_scene, value 'dataset_path'
    of the l1's to be reprocessed by finding add the l1's in the
    scene select log file and that are in the USGS reprocessed file.
    """
    in_area_chopped_scene_id = set(line.strip() for line in open(in_area_file))
    new_l1 = {} # This is the main data structure that is used later.
    other_blocked_l1 = []
    with open(log_file) as f:
        for line in f:
            line_dict = json.loads(line)
            #print (line_dict)
            chopped_scene = chopped_scene_id(line_dict['landsat_scene_id'])
            if chopped_scene in in_area_chopped_scene_id:
                new_l1[chopped_scene] = line_dict['dataset_path']
                in_area_chopped_scene_id.remove(chopped_scene)
            else:
                other_blocked_l1.append(line)
    # Check that all the scenes from the USGS file
    # are being held back from processing
    assert len(in_area_chopped_scene_id) == 0
    return new_l1, other_blocked_l1

def build_l1_info(dc, new_l1, processed_ard_scene_ids, product):
    """
    Build a dict with all the info of new l1 old ARD pairs.  
    l1_new_dataset_path - R2.1 Needed for the list of tars to ARD process
    "ard_old_dataset_yaml - used for moving out of the way
    ard_old_uuid - R2.2b updating and archiving
    """

    grouped_data = {}
    for chopped_scene, l1_ard_path in new_l1.items():
        if chopped_scene in processed_ard_scene_ids:
            ard_old_uuid = processed_ard_scene_ids[chopped_scene]['id']
            a_dataset_list = list(dc.index.datasets.search(id=ard_old_uuid, product=product))
            assert len(a_dataset_list) == 1
            a_dataset = a_dataset_list[0]
            #file_path = (dataset.local_path.parent.joinpath(dataset.metadata.landsat_product_id).with_suffix(".tar").as_posix())
            grouped_data[chopped_scene] = {
                "l1_new_dataset_path":l1_ard_path,
                "ard_old_dataset_yaml":a_dataset.local_path,
                "ard_old_uuid":str(ard_old_uuid),            
            }
    return grouped_data

#### END OF FUNCTIONS ####

def main():
    
    dc = datacube.Datacube(app="gen-list")
    
    # Based on info from the USGS and filtered to
    # Australia's area of intereset
    in_area_file = "in_area_19shr_chopped_scene_id.txt"
    log_file = 'reprocess_all.txt'

    product='ga_ls8c_ard_3'
    processed_ard_scene_ids = calc_processed_ard_scene_ids(dc, product)
    new_l1, other_blocked_l1 = generate_new_l1s(log_file, in_area_file)

    write_2_file(other_blocked_l1, 'rejected_2_reprocess_all.txt')

    grouped_data = build_l1_info(dc, new_l1, processed_ard_scene_ids, product)

    base = "/g/data/xu18/ga/" 
    uuid_file = "old_ards_to_archive.txt"
    old_ard_yaml_file = "old_ard_yaml.txt"
    l1_new_dataset_file = "l1_new_dataset_path.txt"
    files_out(grouped_data,
              uuid_file,
              old_ard_yaml_file,
              l1_new_dataset_file,
              base)

    the_file = 'grouped_data_all.jsonpickle'
    write_dic(grouped_data, the_file)


    
if __name__ == "__main__":
    main()
