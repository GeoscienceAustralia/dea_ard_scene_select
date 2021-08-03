ard-scene-select: select scenes to be processed by ARD
=======================================================

Module creation
---------------
Overall execute `dea-ard-scene-select/modules/go.exe` to generate a new module.

Change `echo "dea_module_dir = ${dea_module_dir:=/g/data/v10/public/modules}"` to change the destination location of the module.
=======
ard-scene-select:
=======================================================

This code is used to select scenes to be processed by ARD. This Repo is deployed as a module to run at NCI.  It is used in production to generate Landsat collection 3 ARD.

Branch Structure
^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Branches
   :header: "Branch name", "Use"

   "master", "The latest reviewed code."
   "production", "The code version used in production. It is the .env files that are used in production."
   "develop", "The development branch."

Currently `develop` code is pushed to `production`.
When Ops has more developers push to `master` then `production`.
Modules are built of the develop branch. Create an annotated tag to tag a module build.
e.g.

    git tag -a "ard-scene-select-py3-dea/20201126" -m "my version 20201126"


Production modules must be built as the `lpgs` user. This can be done using this sandbox;

    /home/547/lpgs/sandbox/dea-ard-scene-select

To produce the module run this script;

    dea-ard-scene-select/modules/go.sh

To update the .env files used in production manually git pull from the production branch at this location;

   /g/data/v10/projects/c3_ard/dea-ard-scene-select/

