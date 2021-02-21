#!/usr/bin/env python

"""hierarchy aval: Realize evalution hierarchy design patter"""

__author__      = "Alan Veloso"
__copyright__   = "Copyright (c) 2020 Alan Veloso"
__license__     = "MIT"
__email__       = "alantsv@gmail.com"

import math
import numbers
from functools import reduce
import sys, getopt
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import random
from networkx.utils import nodes_or_number, py_random_state
import csv
import os
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
sys.path.insert(1, './lib')
from hierarchy_pos import hierarchy_pos

def  random_hierarchy(num_nodes):
    return nx.generators.trees.random_tree(num_nodes)

def coupling_factor (G):
    return float(len(G.edges)/(pow(len(G.nodes),2) - len(G.nodes)))

def main(graphic = True):
    amt_samples = 30
    samples_list = list()
    max_num_class = 10
    name = 'hierarchy'
    data_path = './data'
    plot_path = './plots/{}'.format(name)


    if (graphic == True):
        try:
            os.makedirs(plot_path)
        except OSError:
            print ("Creation of the directory %s failed" % plot_path)
        else: 
            print ("Successfully created the directory %s " % plot_path)

    while (len(samples_list) < amt_samples):
        num_nodes = random.randint(2, max_num_class)
        hierarchy = random_hierarchy(num_nodes)

        check = True
        for i in range(len(samples_list)):
            if (nx.is_isomorphic(hierarchy, samples_list[i])):
                check = False
                break

        if not check:
            continue
        
        samples_list.append(hierarchy)

        if (graphic == True):
            plt.clf()
            nx.draw(
            hierarchy, 
            pos = hierarchy_pos(hierarchy,1), 
            with_labels=True
            )
            filename = '{}/{}-{}.png'.format(plot_path, name,len(samples_list))
            plt.savefig(filename)
    
    try:
        os.mkdir(data_path)
    except OSError:
        print ("Creation of the directory %s failed" % data_path)
    else: 
        print ("Successfully created the directory %s " % data_path)
    
    with open('{}/{}.csv'.format(data_path, name), 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["num", "num_classes", "num_clients", "coupling_factor"])
        [writer.writerow([i+1, len(samples_list[i].nodes), len(samples_list[i].edges), coupling_factor(samples_list[i])]) for i in range(len(samples_list))]
    

if __name__ == "__main__":
    main()