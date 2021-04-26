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

nruns=100

percent = np.zeros((nruns*4,2))
for run_num in range(1, nruns+1):
    hic = pd.read_csv("../data/data_stdev%s/tmp%s/test_beta%s.hic"%(stdev,run_num,beta), sep="\t", header=None)
    hic.columns = ['chr1', 'pos1', 'chr2', 'pos2', 'pval']
    hic = hic[hic['pval']<0.05]
    for i,weight in enumerate([0,1,10,100]):
        gbr = pd.read_csv("../segway-gbr/segway_gbr/out%s/POSTDIR_W%s_B%s_%s/segway.bed"%(stdev,weight, beta, run_num), sep="\t",skiprows=1, header=None)
        pred = transform_pred(gbr)
        hic['same'] = np.absolute(pred[hic['pos1']] - pred[hic['pos2']])

        percent[i,0] = weight
        percent[i,1] = np.sum(hic['same']==0)/hic.shape[0]



percent = pd.DataFrame(percent, columns=["weight", "percent"])
percent.to_csv("./outfiles/weights_stdev%s_b%s.csv" % (stdev, beta))


sns.boxplot(data=percent)
plt.savefig("./figures/weights_boxplot%s_b%s.png"%(stdev, beta)) 
plt.close()