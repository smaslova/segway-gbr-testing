import numpy as np
import pandas as pd

def save_bedgraph(data, outdir, filename):
    """
    Saves data file in bedgraph format. 

    Parameters:
    data (pandas.DataFrame): Dataframe to save; the first column is the label
    the rest are simulated data tracks
    filename (str): name of file where data will be saved
    """
    num_positions = data.shape[0]
    data.insert(loc=0, column='chr', value=np.full(num_positions, 'chr1'))
    data.insert(loc=1, column='start', value=np.arange(num_positions))
    data.insert(loc=2, column='end', value=data['start']+1)

    data[['chr', 'start', 'end', 'track']].to_csv(outdir+filename, sep="\t", header=False, index=False)
    
    include_coords = pd.DataFrame({'chr':['chr1'], 'start':[0], 'end':num_positions}) 
    include_coords.to_csv(outdir + "include-coords.bed", sep="\t", header=False, index=False)

def save_hic(hic_data, filename):
    hicdf = pd.DataFrame(hic_data)
    hicdf = hicdf.reset_index().melt('index')
    hicdf.insert(loc=0, column='chr', value=np.full(hicdf.shape[0], 'chr1'))
    hicdf.insert(loc=2, column='chr2', value=np.full(hicdf.shape[0], 'chr1'))

    hicdf.to_csv(filename, sep="\t", header=False, index=False) 