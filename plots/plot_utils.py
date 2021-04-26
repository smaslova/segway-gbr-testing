import numpy as np


def transform_pred(segway_output):
    pred = []
    for i in range(segway_output.shape[0]):
        for j in range(int(segway_output.iloc[i,1]), int(segway_output.iloc[i,2])):
            pred.append(segway_output.iloc[i,3])

    pred = np.stack(pred)
    return pred

def get_label_numbers(pred, track):
    out = np.array(pred.copy())
    for label in np.unique(pred):
        label_mean = np.rint(np.mean(track[pred==label]))
        out[pred==label] = label_mean
    return out

def get_squared_error(data1, data2):
    #calculate difference
    diff = np.mean(np.square(data1 - data2))
    return np.mean(diff)
