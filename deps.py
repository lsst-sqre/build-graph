#!/usr/bin/env python

import sys
from graphviz import Digraph

manifest = sys.argv[1]

dot = Digraph(comment='lsst_build', format='png')

# format of the manifest.txt file is
# product | sha | version | deps
# Eg.,
#
# pymssql  b098d072...  2.0.0+5  python,freetds
#
# Example of a product without any deps
#
# cfitsio  9799952... 3360.lsst1

with open(manifest) as man:
    for line in man:
        # skip comment lines
        if '#' in line:
            continue

        # skip lines with to few or too many columns
        cols = line.split()
        if len(cols) < 3 or len(cols) > 4:
            continue

        # create a node for the product
        # we do this even for products without deps as they could be orphans
        # without any edges
        product = cols[0]
        dot.node(product)

        # if there is a forth column, it is a list of dependencies. Otherwise,
        # we are done processing this line.
        if len(cols) < 4:
            continue

        # add an edge for each dep
        deps = cols[3].split(',')
        for req in deps:
            dot.edge(product, req)

dot.render("deps.dot")
