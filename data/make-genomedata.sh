#!/bin/bash

DIR="./data_stdev${5}/tmp${4}"
TRACK1=${DIR}/${1}
TRACK2=${DIR}/${2}
OUT=${DIR}/${3}

genomedata-load --sequence=chr1.fa --track=testtrack1=$TRACK1 --track=testtrack2=$TRACK2 --file-mode --verbose $OUT 