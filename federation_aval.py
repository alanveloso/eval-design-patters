#!/usr/bin/env python

"""federation aval: Realize evalution federation design patter"""

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

@py_random_state(3)
def random_federation(num_buyer, num_seller, p, seed=None):
    """Returns a bipartite random graph.

    This is a bipartite version of the binomial (Erdős-Rényi) graph.
    The graph is composed of two partitions. Set A has nodes 0 to
    (n - 1) and set B has nodes n to (n + m - 1).

    Parameters
    ----------
    n : int
        The number of nodes in the first bipartite set.
    m : int
        The number of nodes in the second bipartite set.
    p : float
        Probability for edge creation.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    directed : bool, optional (default=False)
        If True return a directed graph

    Notes
    -----
    The bipartite random graph algorithm chooses each of the n*m (undirected)
    or 2*nm (directed) possible edges with probability p.

    This algorithm is $O(n+m)$ where $m$ is the expected number of edges.

    The nodes are assigned the attribute 'bipartite' with the value 0 or 1
    to indicate which bipartite set the node belongs to.

    This function is not imported in the main namespace.
    To use it use nx.bipartite.random_graph
    """
    G = nx.DiGraph()

    def _add_nodes_with_bipartite_label(G, lena, lenb):
        G.add_nodes_from(range(0, lena + lenb))
        b = dict(zip(range(0, lena), [0] * lena))
        b.update(dict(zip(range(lena, lena + lenb), [1] * lenb)))
        nx.set_node_attributes(G, b, "bipartite")
        return G

    G = _add_nodes_with_bipartite_label(G, num_buyer, num_seller)
    G.name = f"fast_gnp_random_graph({num_buyer},{num_seller},{p})"
    
    if p <= 0:
        return G
    if p >= 1:
         return nx.complete_bipartite_graph(num_buyer, num_seller) 

    lp = math.log(1.0 - p)

    v = 0
    w = -1
    while v < num_buyer:
        lr = math.log(1.0 - seed.random())
        w = w + 1 + int(lr / lp)
        while w >= num_seller and v < num_buyer:
            w = w - num_seller
            v = v + 1
        if v < num_buyer:
            G.add_edge(v, num_buyer + w)

    return G

def coupling_factor (G):
    return float(len(G.edges)/(pow(len(G.nodes),2) - len(G.nodes)))

def main(graphic = True):
    amt_samples = 30
    samples_list = list()
    min_num_class = 1
    total_num_class = 10
    name = 'federation'
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
        num_buyer = random.randint(min_num_class, total_num_class - min_num_class)
        num_seller = random.randint(min_num_class, total_num_class - num_buyer)
        federation = random_federation(num_buyer, num_seller, 0.5)
        
        if not nx.is_weakly_connected(federation):
            continue
    
        check = True
        for i in range(len(samples_list)):
            if (nx.is_isomorphic(federation, samples_list[i])):
                check =  False
                break

        if not check:
            continue
        samples_list.append(federation)

        if (graphic == True):
            plt.clf()
            buyer_nodes, _ = nx.algorithms.bipartite.sets(federation)
            nx.draw_networkx(
            federation,
            pos = nx.drawing.layout.bipartite_layout(federation, buyer_nodes),
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
