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
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
sys.path.insert(1, './lib')
from hierarchy_pos import hierarchy_pos

@py_random_state(1)
def random_hierachy(n, seed=None):
    """Returns a uniformly random tree on `n` nodes.

    Parameters
    ----------
    n : int
        A positive integer representing the number of nodes in the tree.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    NetworkX graph
        A tree, given as an undirected graph, whose nodes are numbers in
        the set {0, …, *n* - 1}.

    Raises
    ------
    NetworkXPointlessConcept
        If `n` is zero (because the null graph is not a tree).

    Notes
    -----
    The current implementation of this function generates a uniformly
    random Prüfer sequence then converts that to a tree via the
    :func:`~networkx.from_prufer_sequence` function. Since there is a
    bijection between Prüfer sequences of length *n* - 2 and trees on
    *n* nodes, the tree is chosen uniformly at random from the set of
    all trees on *n* nodes.

    """
    if n == 0:
        raise nx.NetworkXPointlessConcept("the null graph is not a tree")
    # Cannot create a Prüfer sequence unless `n` is at least two.
    if n == 1:
        return nx.empty_graph(1)
    sequence = [seed.choice(range(n)) for i in range(n - 2)]
    return nx.from_prufer_sequence(sequence)


def main(graphic = True):
    plt.clf()
    G = random_hierachy(10)
    print(G)
    
    nx.draw(G, 
    pos = hierarchy_pos(G,1), 
    with_labels=True)
    plt.savefig('hierarchy.png')
    

if __name__ == "__main__":
    main()