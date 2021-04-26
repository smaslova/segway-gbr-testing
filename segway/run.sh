#!/bin/bash

RUNNUM=$4
INDIR="../data/data_stdev${5}/tmp${RUNNUM}"
INPUT=${1}
traindir=${2}${RUNNUM}
posteriordir=${3}${RUNNUM}
stdev=${5}

rm -rf $traindir 
rm -rf $posteriordir

echo "SEGWAY"
echo "TRAIN: ${traindir}"
echo "POST: ${posteriordir}"

module load nixpkgs/16.09  gcc/5.4.0 gmtk python/3.8.0
source ~/py38/bin/activate

segway train --num-labels=2 --include-coords=${INDIR}/include-coords.bed ${INDIR}/${INPUT} $traindir

segway posterior ${INDIR}/${INPUT} $traindir $posteriordir


gunzip ${posteriordir}/segway.bed.gz
mv ${posteriordir}/segway.bed ${traindir}
rm -r ${posteriordir}/* 
mv ${traindir}/segway.bed ${posteriordir}
rm -r ${traindir}
