#!/usr/bin/env bash
# Convenience script for running black
# potentially get this going in .pre-commit-config.yaml
module use /g/data/v10/public/modules/modulefiles
module load dea

black -l 120  tests/ scene_select/ scripts/
