#!/usr/bin/env python3

import datacube
from datetime import datetime

print("normal")
print("before search =", datetime.now())
dc = datacube.Datacube(app="gen-list")
for dataset in dc.index.datasets.search(product="usgs_ls5t_level1_1"):
    print(dataset.metadata.landsat_product_id)
    print("after search =", datetime.now())
    break
