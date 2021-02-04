#!/usr/bin/env python3
"""
Load a csv with PATH	ROW	YEAR	DOY columns.
Output to standard out only the (path, row) rows that are in the Australian area of interest.
"""
from pathlib import Path
from typing import List, Tuple, Optional
import csv
from collections import defaultdict
import datetime
import os

def load_aoi_oz(allowed_codes: Path) -> List:
    """ Convert a file of allowed codes to a list of region codes. """
    with open(allowed_codes, "r") as fid:
        path_row_list = [line.rstrip() for line in fid.readlines()]
    path_row_list = ["{:03}{:03}".format(int(item.split("_")[0]), int(item.split("_")[1])) for item in path_row_list]
    return path_row_list


def load_aoi_usgs2(allowed_codes: Path) -> List:
    with open(allowed_codes, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        data = list(reader)
    path_row_list = [(item[0])  + (item[1]) for item in data]
    path_row_dic =  defaultdict(list)
    file_label_dic =  defaultdict(list)
    general_dic =  defaultdict(list)
    path = 0
    row = 1
    year = 2
    ytd = 3
    for item in data:
        # Build up a dict of dicts
        the_date = datetime.datetime(int(item[2]), 1, 1) + datetime.timedelta(int(item[3]) - 1)
        path_row_dic[((item[0])+(item[1]))].append((datetime.datetime(int(item[2]), 1, 1) + datetime.timedelta(int(item[3]) - 1), 'day: ' + item[3]))
        file_label_dic[((item[0])+(item[1]))].append(item[path] + item[row] + \
                                                     '_' + the_date.strftime('%Y%m%d'))
        a_scene = {
            'path':item[path],
            'row':item[row],
            'year':item[year],
            'ytd':item[ytd],
            'the_date':the_date}
        general_dic[((item[0])+(item[1]))].append(a_scene)
    return path_row_dic, file_label_dic, general_dic


if __name__ == "__main__":    
    aoi_oz = "Australian_Wrs_list_without_113_070.txt"
    oz_set = load_aoi_oz(aoi_oz)
    #print (path_row_list)
    
    usgs = 'usgs_reprocess.csv'
    usgs_dic, file_dic, general_dic = load_aoi_usgs2(usgs)
    #print (usgs_dic)
    #print (usgs_set.intersection(oz_set))
    if False:
        for key, value in usgs_dic.items():
            if key in oz_set:
                print (key, value)
    # remove all the path rows outside AOI            
    for key in list(general_dic):
        if key not in oz_set:
            del general_dic[key]
    #print (len(general_dic)) # 220

    f_scene_id = open("in_area_19shr_chopped_scene_id.txt", "w")
    for key, value in general_dic.items():
        assert len(value) == 1
        value = value[0]
        chopped_scene_id = "LC8" + value['path']  + value['row'] + value['year'] + value['ytd'] + "\n"
        f_scene_id.write(chopped_scene_id)
    f_scene_id.close()
