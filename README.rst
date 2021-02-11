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
   "production", "The code version used in produciton. It is the .env files that are used in production."
   "develop", "The development branch."

Modules are built of the develop branch. Create an annotated tag to tag a module build.
e.g.

    git tag -a "ard-scene-select-py3-dea/20201126" -m "my version 20201126"

