#!/usr/bin/env python

import sys
from graphviz import Digraph

manifest = sys.argv[1]

dot = Digraph(comment='lsst_build', format='png')

with open(manifest) as man:
    for line in man:
        if '#' in line:
            continue

        cols = line.split()
        if len(cols) < 4:
            continue

        product = cols[0]
        deps = cols[3].split(',')

        dot.node(product)
        for req in deps:
            dot.edge(product, req)

dot.render("deps.dot")
