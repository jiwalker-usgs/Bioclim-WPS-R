#!/bin/bash

path_file=$1
paths=$(cat ${path_file})

for p in ${paths}; do

    model=$(echo ${p} | sed 's/\// /g' | awk '{print $2}')
    rcp=$(echo ${p} | sed 's/\// /g' | awk '{print $3}')
    run=$(echo ${p} | sed 's/\// /g' | awk '{print $5}')

    #GCMUPPER=$(echo ${model} | tr '[:lower:]' '[:upper:]')
    #echo "$model ${GCMUPPER} $run"

    echo "${model} ${run} ${rcp}"
    bin/fix_bcca_pr_bias_apply_ratios.sh ${model} ${run} ${rcp}

#exit

done
