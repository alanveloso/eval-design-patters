#!/usr/bin/env python

"""market aval: Realize evalution market design patter"""

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
def random_market(num_buyer, num_seller, p, seed=None):
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

    See Also
    --------
    gnp_random_graph, configuration_model

    References
    ----------
    .. [1] Vladimir Batagelj and Ulrik Brandes,
       "Efficient generation of large random networks",
       Phys. Rev. E, 71, 036113, 2005.
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

def main(graphic = False):
    amt_samples = 30
    set_samples = set()
    min_num_class = 1
    total_num_class = 10
    file_name = 'market_validation'

    if (graphic == True):
        path = './plots/market'
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else: 
            print ("Successfully created the directory %s " % path)

    while (len(set_samples) < amt_samples):
        num_buyer = random.randint(min_num_class, total_num_class - min_num_class)
        num_seller = random.randint(min_num_class, total_num_class - num_buyer)
        market = random_market(num_buyer, num_seller, 0.5)
        try:
            buyer_nodes, seller_nodes = nx.algorithms.bipartite.sets(market)
            set_samples.add((len(set_samples)+1, num_buyer + num_seller, len(market.edges), coupling_factor(market)))

            if (graphic == True):
                plt.clf()
                nx.draw_networkx(
                market,
                pos = nx.drawing.layout.bipartite_layout(market, buyer_nodes),
                )
                filename = 'plots/market/market-{}.png'.format(len(set_samples))
                plt.savefig(filename)
        except:
            pass
    
    with open('{}.csv'.format(file_name), 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["num", "num_classes", "num_clients", "coupling_factor"])
        [writer.writerow(list(r)) for r in set_samples]

if __name__ == "__main__":
    main()
