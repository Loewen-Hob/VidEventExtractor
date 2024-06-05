#! /bin/bash

NUM_GPUS=$1
shift

python3 run_dee_task.py $*
