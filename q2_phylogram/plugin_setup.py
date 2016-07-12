# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
"""
description:

    Helper script for generating all the files needed to view
    the interactive D3 phylogram (https://github.com/ConstantinoSchillebeeckx/phylogram_d3).

examples:

    make_d3_phylogram.py newick.tre -m otu_mapping.txt
    make_d3_phylogram.py newick.tre -m otu_mapping.txt -o data_dir

"""
import importlib

import qiime.plugin

from q2_phylogram import __version__

# IMPORTS
import sys, os, argparse, traceback
import pandas as pd
from Bio import Phylo

template = '''
<!doctype html>

<html lang="en">

    <head>

        <!-- CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Open+Sans" />
        <link href="https://cdn.rawgit.com/MasterMaps/d3-slider/master/d3.slider.css" rel="stylesheet">
        <link href="https://cdn.rawgit.com/ConstantinoSchillebeeckx/phylogram_d3/master/css/phylogram_d3.css" rel="stylesheet">

        <!-- JS -->
        <script type="text/javascript" src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
        <script type="text/javascript" src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/mbostock/5577023/raw/5ee09dca6afdbef864de89d4d6caa3296f926f00/colorbrewer.min.js "></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/jasondavies/newick.js/master/src/newick.js"></script>
        <script src="https://d3js.org/d3.v3.min.js"></script>
        <script src="http://labratrevenge.com/d3-tip/javascripts/d3.tip.v0.6.3.js"></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/MasterMaps/d3-slider/master/d3.slider.js"></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/ConstantinoSchillebeeckx/phylogram_d3/master/js/phylogram_d3.js"></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/ConstantinoSchillebeeckx/phylogram_d3/master/js/utils.js"></script>

        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>

    REPLACE

        <!-- div for tree -->
        <div id='phylogram'></div>

    </body>
</html>
'''


# ------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------- MAIN -----------------------------------------------------#
# ------------------------------------------------------------------------------------------------------------#
def make_d3_phylogram(args):

    # ERROR CHECK INPUTS
    if args.mapping:

        tree = Phylo.read(args.newick, 'newick')
        leaves = set([l.name for l in tree.find_clades() if l.name])

        mapping_df = pd.read_csv(args.mapping, sep='\t', index_col=0)
        mapping_otus = set(mapping_df.index)

        if leaves > mapping_otus:
            print("Not all leaves were found in the OTU mapping file; as a consequence, these leaves cannot be styled.")


    # CONSTRUCT BODY TAG
    if args.mapping:
        body = '<body onload="init(\'dat/tree.tre\', \'#phylogram\', \'dat/mapping.txt\');">' 
    else:
        body = '<body onload="init(\'dat/tree.tre\', \'#phylogram\');">' 

    index = template.replace('REPLACE',body) # html to write to index.html


    # WRITE ALL OUR FILES
    root = os.path.join(args.out,'phylogram_d3')
    out_dir = os.path.join(root,'dat')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(os.path.join(root,'index.html'), 'w') as fout:
        fout.write(index)
    os.system('cp %s %s/tree.tre' %(args.newick, out_dir))
    if args.mapping:
        os.system('cp %s %s/mapping.txt' %(args.mapping, out_dir))


    # FEEDBACK
    print("All your files have been written to the directory", root)
    print("Simply open the file index.html in a browser that has")
    print("an internet connection to view the interactive phylogram.")



plugin = qiime.plugin.Plugin(
    name='phylogram',
    version=__version__,
    website='https://github.com/ConstantinoSchillebeeckx/q2-phylogram',
    package='q2_phylogram'
)

plugin.visualizers.register_function(
    function=make_d3_phylogram,
    inputs={'Newick_tree': newick},
    parameters={'OTU_metadata': metadata},
    name='Visualize phylogram',
    description='Generate interactive visualization of your phylogenetic tree.'
)
