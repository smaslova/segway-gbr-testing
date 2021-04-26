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
seg_error = []
sgbr_error = []

for run_num in range(1, nruns+1):
    data = pd.read_csv("../data/data_stdev%s/tmp%s/simulated_data.csv"%(stdev,run_num))
    seg = pd.read_csv("../segway/out%s/posteriordir%s/segway.bed"%(stdev,run_num), sep="\t",skiprows=1, header=None)
    gbr = pd.read_csv("../segway-gbr/segway_gbr/out%s/POSTDIR_W%s_B%s_%s/segway.bed"%(stdev,weight, beta, run_num), sep="\t",skiprows=1, header=None)

    seg_pred = transform_pred(seg)
    data['segway_pred'] = get_label_numbers(seg_pred, data['track1'].values)

    gbr_pred = transform_pred(gbr)
    data['sgbr_pred'] = get_label_numbers(gbr_pred, data['labels'].values)

    #calculate error
    seg_error.append(get_squared_error(data['segway_pred'], data['labels']))
    sgbr_error.append(get_squared_error(data['sgbr_pred'], data['labels']))

error = pd.DataFrame({'seg_error':seg_error, 'sgbr_error':sgbr_error})
error.to_csv("./outfiles/error_stdev%s_b%s_w%s.csv"% (stdev, beta, weight))

sns.boxplot(data=error)
plt.savefig("./figures/error_boxplot%s_b%s_w%s.png"%(stdev, beta, weight))
plt.close()

sns.scatterplot(x='seg_error', y='sgbr_error', data=error)
plt.savefig("./figures/error_scatterplot%s_b%s_w%s.png"%(stdev, beta, weight))
plt.close()

