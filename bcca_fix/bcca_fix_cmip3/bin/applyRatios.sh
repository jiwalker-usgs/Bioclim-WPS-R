#!/bin/bash

# This script takes a file linsting paths to files that should be processed.
# It calls a function that executes cdo command.

path_file=$1
paths=$(cat ${path_file})

for p in ${paths}; do

    model=$(echo ${p} | sed 's/\// /g' | awk '{print $2}')
    rcp=$(echo ${p} | sed 's/\// /g' | awk '{print $3}')
    run=$(echo ${p} | sed 's/\// /g' | awk '{print $4}')

    echo "${model} ${run} ${rcp}"
    bin/fix_bcca_pr_bias_apply_ratios.sh ${model} ${run} ${rcp}

#exit

done
