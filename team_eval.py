#!/usr/bin/env python

"""team aval: Realize evalution team design patter"""

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

def random_team (n, p):
    return nx.gnp_random_graph(n,p,directed=True)

def coupling_factor (G):
    return float(len(G.edges)/(pow(len(G.nodes),2) - len(G.nodes)))

def main(graphic = True):
    amt_samples = 30
    samples_list = list()
    total_num_class = 10
    prob = 0.5
    name = 'team'
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
        num_nodes = random.randint(2, total_num_class)
        team = random_team(num_nodes, prob)
        
        if not nx.is_weakly_connected(team):
            continue

        check = True
        for i in range(len(samples_list)):
            if (nx.is_isomorphic(team, samples_list[i])):
                check = False
                break

        if not check:
            continue
        samples_list.append(team)

        if (graphic == True):
            plt.clf()
            #buyer_nodes, _ = nx.algorithms.bipartite.sets(team)
            nx.draw_networkx(
            team
            #pos = nx.drawing.layout.bipartite_layout(team, buyer_nodes),
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