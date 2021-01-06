#!/usr/bin/env python3

"""
OOAOI - Out of Australian area of interest.
"""

import json

import datacube

log_file = '/g/data1a/u46/users/dsg547/sandpit/dea-ard-scene-select/scripts/examples/scratch/filter-jobid-e515b2/ard_scene_select.log'


uuids = []
sum = 0
with open(log_file) as f:
    for line in f:
        line_dict = json.loads(line)
        #print (line_dict)
        if 'reason' in line_dict and line_dict['reason'] == "Region not in AOI":
            sum += 1
            uuid_long = line_dict['uuid']
            uuid_list = uuid_long.split("'")
            uuids.append(uuid_list[1])
         
print (sum)

for a_uuid in uuids:
    pass

f_out = open("myfile.txt", "w")
for a_uuid in uuids:
    f_out.write(a_uuid + '\n')
f_out.close() 
