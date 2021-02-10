#!/usr/bin/env python3

import os
import stat
import math
from pathlib import Path
from typing import List, Tuple, Optional
import re
import uuid
import subprocess
import datetime
import click
import pprint

import datacube


@click.command()
@click.option(
    "--config",
    type=click.Path(dir_okay=False, file_okay=True),
    help="Full path to a datacube config text file. This describes the ODC database.",
    default=None,
)
@click.option(
    "--uuidfile",
    type=click.Path(dir_okay=False, file_okay=True),
    help="he uuids of scenes to be moved",
)
@click.option(
    "--stagingdir",
    type=click.Path(file_okay=False, writable=True),
    help="The base output working directory.",
    default=Path.cwd(),
)
@click.option(
    "--ardbasedir",
    type=click.Path(file_okay=False, writable=True),
    help="The base working directory of the ard files.",
    default=Path.cwd(),
)
def connect(
    config: click.Path, uuidfile: click.Path, stagingdir: click.Path, ardbasedir: click.Path,
):
    dc = datacube.Datacube(app="gen-list", config=config)

    old_uri = "file:///g/data/u46/users/dsg547/test_data/c3/LC81150802019349/" \
        "LC08_L1TP_115080_20191215_20201023_01_T1.odc-metadata.yaml"
    new_uri = "file:///g/data/u46/users/dsg547/test_data/c3_dump/LC81150802019349/" \
        "LC08_L1TP_115080_20191215_20201023_01_T1.odc-metadata.yaml"
    dataset_gen = dc.index.datasets.get_datasets_for_location(uri=old_uri)
    # with open(log_file) as f:
    #   for line in f:
    for a_dataset in dataset_gen:
        pprint.pprint(a_dataset)

    dc.index.datasets.update(new_uri)

    for a_dataset in dataset_gen:
        pprint.pprint(a_dataset)


if __name__ == "__main__":
    connect()
