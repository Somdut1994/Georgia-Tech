from scipy import stats
import numpy as np

# This method computes entropy for information gain
def entropy(class_y):
    """Compute the entropy for a list of classes

    Example:
        entropy([0,0,0,1,1,1,1,1,1]) = 0.92
    """
    # TODO: Implement this
    if len(class_y) ==0:
        return 0
    else:
        frac=float(sum(class_y))/len(class_y)
        if frac ==1 or frac==0:
            return 0
        else: 
            return -(frac*np.log2(frac) + (1-frac)*np.log2((1-frac)))

def partition_classes(x, y, split_point):
    """Partition the class vector, y, by the split point. 

    Return a list of two lists where the first list contains the labels 
    corresponding to the attribute values less than or equal to split point
    and the second list contains the labels corresponding to the attribute 
    values greater than split point

    Example:
    x = [2,4,6,7,3,7,9]
    y = [1,1,1,0,1,0,0]
    split_point = 5

    output = [[1,1,1], [1,0,0,0]]
    """
    output=[[],[]]
    # TODO: Implement this
    for i in range(0,len(x)):
        if x[i]<=split_point:
            output[0].extend([y[i]])
        else:
            output[1].extend([y[i]])
    return output
 
def information_gain(previous_y, current_y):
    """Compute the information gain from partitioning the previous_classes
    into the current_classes.

    Example:
    previous_classes = [0,0,0,1,1,1]
    current_classes = [[0,0], [1,1,1,0]]

    Information gain = 0.45915
    Input:
    -----
        previous_classes: the distribution of original labels (0's and 1's)
        current_classes: the distribution of labels given a particular attr
    """
    # TODO: Implement this
    E_p = entropy(previous_y)
    frac = float(len(current_y[0]))/(len(current_y[0])+len(current_y[1]))
    E_c = frac*entropy(current_y[0]) + (1-frac)*entropy(current_y[1])
    return (E_p-E_c)
    

