#!/bin/bash

#Setting up the test db
#./go_add.sh

# The steps in step 1
# Step 1 – duplicate dataset to be archived in staging area
# 1.       Duplicate the [to be] archived dataset in “staging for removal” location”

#2.       Update location [in ODC] to point to
#         location in “staged for removal location”
# Note this is initially setup to just run on the test db
# edit ../step1.sh to change the base dirs

# ./go_step1.sh # steps 1.1 and 1.2
#3.       Wait prerequisite flush period (until queue empties) - 2 hours?
#4.       Trash original
