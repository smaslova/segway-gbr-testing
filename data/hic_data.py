import numpy as np

class HicData():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def simulate_hic(self, labels):
        """
        Returns p-value for statistical significance of contact between every pair of positions in labels

        Parameters:
        labels (ndarray): 1D array containing data of 'int' type.
        """
        a = self.a
        b = self.b
        num_positions = labels.shape[0]

        #difference between labels; 0 if labels are the same, 1 if labels are different
        cols = np.array([labels,]*num_positions)
        rows = cols.transpose()
        diff = np.absolute(rows-cols)
        diff[diff>0] = 1

        #p-values uniformly distributed for different labels
        hic1 = np.random.uniform(low=0, high=1, size=(num_positions, num_positions))
        
        #p-values beta-distributed for same labels
        hic2 = np.random.beta(a, b, size=(num_positions, num_positions))

        hic = np.multiply(hic1, diff) + np.multiply(hic2, (1-diff))

        return hic


        