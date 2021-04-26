#!/bin/bash

module load nixpkgs/16.09  gcc/5.4.0 gmtk python/3.8.0
source ~/py38/bin/activate

beta=75
for weight in 0, 1, 10, 100
do
  for stdev in 0.5, 1.0, 1.5, 2.0
  do
    python plot_replicates.py $stdev $beta $weight
    python plot_swaps.py $stdev $beta $weight
    python plot_reverse.py $stdev $beta $weight
  done
  
  python error_plots.py $beta $weight
  python MR1_plot.py $beta $weight
  python MR2_plot.py $beta $weight
done

for stdev in 0.5, 1.0, 1.5, 2.0
do 
  python plot_weight.py $stdev $beta
done

python MR2_plot.py $beta