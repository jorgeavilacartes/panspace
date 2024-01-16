"""
Partition an input list of files into 5 subsets. 
Output .txt files with the partitions to be used for training an autoencoder.
"""
import random
import numpy as np

from collections import defaultdict


class CrossValidationSplit:

    def __init__(self, kfolds: int = 5, seed=42):
        random.seed(seed) #reproducibility
        self.kfolds = kfolds


    def __call__(self, list_paths: list):
        "Return a dictionary with all partitions"
        random.shuffle(list_paths)  # randomize positions of list_paths
        
        # split list_paths in the number of k-folds selected
        idx_kfolds = np.array_split(range(len(list_paths)), self.kfolds)

        paths_by_partition = defaultdict(list)
        for j, list_idx in enumerate(idx_kfolds):
            
            for idx in list_idx:
                paths_by_partition[j].append(list_paths[idx])

        return paths_by_partition
