import numpy as np
import pandas as pd
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

beta=sys.argv[1]

data = pd.DataFrame(columns=['stdev', 'weight', 'percent'])

stdevs_tried = ['0.5','1.0','1.5','2.0']
stdevs = [0.5, 1, 1.5, 2] 
for i, stdev in enumerate(stdevs_tried):
    file = "./outfiles/weights_stdev%s_b%s.csv" % (stdev, beta)
    percent = pd.read_csv(file, index_col=0)
    percent.columns=['Percent']
    percent['stdev'] = stdevs[i]
    percent = percent.melt(id_vars=['stdev'], value_vars=["weight", "percent"])
    percent.columns = ['stdev', 'weight', 'percent']

    data = pd.concat([data, percent])


sns.lineplot(data=data, x="weight", y="percent", hue="stdev", err_style="bars", ci='sd'))
plt.xlabel("Weight")
plt.ylabel("Percent Contacts")
plt.tight_layout()
plt.savefig("./figures/combined/MR3_lineplot_b%s_w%s.pdf"%(beta))
plt.close()
