#!/usr/bin/env bash

module use /g/data/v10/public/modules/modulefiles
module load dea

#UUID='10750a97-fe7b-4fe4-8e2c-1441cdafdaaa'
UUID='c5d441d1-6525-439a-936d-469ef0144a22'

datacube dataset info $UUID
datacube  dataset archive $UUID
datacube  dataset info $UUID
