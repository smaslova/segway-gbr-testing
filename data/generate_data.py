import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import seaborn as sns
import sys
import os

from markov_chain import MarkovChain
from hic_data import HicData
from utils import save_bedgraph, save_hic

var = float(sys.argv[1])
run_num = sys.argv[2]

outdir = "data_stdev%s/tmp%s/" % (var,run_num)
try:
    os.makedirs(outdir)
except OSError:
    print ("Directory %s exists" % outdir)
else:
    print ("Successfully created the directory %s" % outdir)

num_tracks = 2
num_positions=1000
transition_prob = {0 : {0:0.95, 1:0.05},
                    1 : {0:0.05, 1:0.95}}

mc = MarkovChain(transition_prob)
labels = mc.generate_states(num_positions)
data = pd.DataFrame({'labels':labels})

for n in range(1, num_tracks+1):
    track = np.array([np.random.normal(state, scale=var) for state in labels])

    filename = "test_track%s.bedgraph" % n
    save_bedgraph(pd.DataFrame({'track':track}), outdir, filename)

    #save reverse:
    filename = "rev_test_track%s.bedgraph" % n
    rev_track = np.flip(track)
    save_bedgraph(pd.DataFrame({'track':rev_track}), outdir, filename)
  
    sns.heatmap(pd.DataFrame({"original":track, "reverse":rev_track, "reverse_flipped":np.flip(rev_track)}), 
                                cmap=sns.color_palette("viridis", as_cmap=True))
    plt.savefig(outdir + "track%s_heatmap.png"%n)
    plt.close()

    data['track%s'%n] = track

data.to_csv(outdir+"simulated_data.csv")



###null hic
#null_hic = np.full(hic.shape, fill_value=1)
#null_hic[np.diag_indices(hic.shape[0], ndim = 2)]=0 
#hic = null_hic
###
a=1
for b in [1, 5, 50, 75]:
    hic_sim = HicData(a, b)
    hic = hic_sim.simulate_hic(labels)

    hicfile = outdir + "test_beta%s.hic" % b
    save_hic(hic, hicfile)

    #save reverse hic:
    hicfile2 = outdir + "rev_test_beta%s.hic" % b
    save_hic(np.flip(hic), hicfile2)

plt.hist(hic.flat, bins=50)
plt.xlabel("p-value")
plt.ylabel("frequency")
plt.tight_layout()
plt.savefig(outdir+"hic_pvals.pdf")
plt.close()

sns.heatmap(hic, cmap=sns.cm.rocket_r)
plt.savefig(outdir+"hic_heatmap.pdf")
plt.close()

sns.heatmap(np.flip(hic), cmap=sns.cm.rocket_r)
plt.savefig(outdir+"rev_hic_heatmap.pdf")
plt.close()




 


