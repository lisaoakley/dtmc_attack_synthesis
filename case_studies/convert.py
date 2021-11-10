#!/usr/bin/env python3

'''
Small utility for converting a PRISM dtmc model file
into an adjacency matrix (transition probability matrix)
to use as input for attack generation.

USAGE: 

./convert.py [prism model file (.pm)] [out file (.csv)]
'''

import logging
import pandas as pd
import numpy as np
import scipy.sparse as sparse
import sys

logging.getLogger().setLevel(level=getattr(logging, "INFO"))

filename = sys.argv[1]
outfile = sys.argv[2]
n_states = 0
n_transitions = 0
edge_list = []

with open(filename) as f:
    data = f.readlines()
    meta = data[0].split()
    n_states = int(meta[0])
    n_transitions = int(meta[1])
    edge_list = np.ndarray([n_transitions,3])
    for i,val in enumerate(data[1:]):
        edge_list[i] = val.split()

st_from, st_to, weight = edge_list[:,0], edge_list[:,1], edge_list[:,2]
adj_mat = sparse.lil_matrix((n_states,n_states))
for i,j,w in zip(st_from,st_to,weight):
    adj_mat[i,j] = w

pd.DataFrame(adj_mat.todense()).to_csv(outfile,index=False,header=False)
logging.info(f'{outfile}')
