import numpy as np
import pandas as pd
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

beta=sys.argv[1]
weight=sys.argv[2]
 
data = pd.DataFrame(columns=['stdev', 'method', 'error'])

stdevs_tried = ['0.5','1.0','1.5','2.0']
stdevs = [0.5, 1.0, 1.5, 2.0] 
for i, stdev in enumerate(stdevs_tried):
    file = "./outfiles/error_stdev%s_b%s_w%s.csv" % (stdev, beta, weight)
    err = pd.read_csv(file, index_col=0)
    err.columns = ["Segway", "Segway-GBR"]
    err['stdev'] = stdevs[i]
    err = err.melt(id_vars=['stdev'], value_vars=["Segway", "Segway-GBR"])
    err.columns = ['stdev', 'method', 'error']

    data = pd.concat([data, err])


sns.barplot( data=data, x="stdev", y="error", hue="method", 
            ci='sd', errwidth=0.2, capsize=.2) # palette="dark",

plt.xlabel("Noise Level")
plt.ylabel("Mean Error")
plt.tight_layout()
plt.savefig("./figures/combined/error_barplot_b%s_w%s.pdf"%(beta, weight))
plt.close()

sns.boxplot( data=data, x="stdev", y="error", hue="method") 
plt.xlabel("Noise Level")
plt.ylabel("Mean Error")
plt.tight_layout()
plt.savefig("./figures/combined/error_boxplot_b%s_w%s.pdf"%(beta, weight))
plt.close()