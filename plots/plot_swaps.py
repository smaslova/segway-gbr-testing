import numpy as np
import pandas as pd
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from plot_utils import get_label_numbers, transform_pred, get_squared_error

stdev=sys.argv[1]
beta=sys.argv[2]
weight = sys.argv[3]

nruns=100
flip_axis=0
seg_diff_all = []
sgbr_diff_all = []

for run_num in range(1, nruns+1):
    data = pd.read_csv("../data/data_stdev%s/tmp%s/simulated_data.csv"%(stdev,run_num))

    seg = pd.read_csv("../segway/out%s/posteriordir%s/segway.bed"%(stdev,run_num), sep="\t",skiprows=1, header=None)
    swap_seg = pd.read_csv("../segway/out%s/swap_posteriordir%s/segway.bed"%(stdev,run_num), sep="\t",skiprows=1, header=None)
    
    gbr = pd.read_csv("../segway-gbr/segway_gbr/out%s/POSTDIR_W%s_B%s_%s/segway.bed"%(stdev,weight, beta, run_num), sep="\t",skiprows=1, header=None)
    swap_gbr = pd.read_csv("../segway-gbr/segway_gbr/out%s/SWAP_POSTDIR_W%s_B%s_%s/segway.bed"%(stdev,weight, beta, run_num), sep="\t",skiprows=1, header=None)
    
    #transform predictions to single bp resolution and get matching segment labels
    seg_pred = get_label_numbers(transform_pred(seg), data['track1'].values)
    swap_seg_pred = get_label_numbers(transform_pred(swap_seg), data['track1'].values)

    gbr_pred = get_label_numbers(transform_pred(gbr), data['track1'].values)
    swap_gbr_pred = get_label_numbers(transform_pred(swap_gbr), data['track1'].values)

    #calculate difference
    seg_diff_all.append(get_squared_error(seg_pred, swap_seg_pred))
    sgbr_diff_all.append(get_squared_error(gbr_pred, swap_gbr_pred))

diff = pd.DataFrame({'segway':seg_diff_all, 'segway-gbr':sgbr_diff_all})
diff.to_csv("./outfiles/swap_diff_stdev%s_b%s_w%s.csv"% (stdev, beta, weight))

sns.boxplot(data=diff)
plt.savefig("./figures/swap_diff_boxplot%s_b%s_w%s.png"%(stdev, beta, weight)) 
plt.close()

sns.scatterplot(x='segway', y='segway-gbr', data=diff)
plt.savefig("./figures/swap_diff_scatterplot%s_b%s_w%s.png"%(stdev, beta, weight))
plt.close()

