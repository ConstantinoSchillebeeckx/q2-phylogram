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

"""
import importlib

import qiime
from qiime.plugin import Plugin
from q2_phylogram import __version__
from q2_types import Phylogeny

# IMPORTS
import sys, os, argparse, traceback
import pandas as pd
import skbio
import skbio.io

template = '''
<!doctype html>

<html lang="en">

    <head>
        <title>q2-phylogram</title>

        <!--
        Note that, when used as a QIIME2 plugin, cross-origin issues could arise when loading local files (e.g. Newick tree
        and mapping file).  To get around this, a seperate version of the init() function is loaded (from q2_phylogram.js)
        that uses JSONP to load the Newick tree.  When this is the case, the tree file contents must be wrapped in the
        d3.jsonp.readNewick() callback function.  Furthermore, the mapping file is parsed into a JSON object and stored as
        as the javascript var within options.mapping_dat.  This should alleviate any cross-origin issues while at the same
        time leaving the original phylogram_d3 repo in its original state (e.g. being able to read classical Newick trees)
        -->

        <!-- CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Open+Sans:400,300,700,800" />
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
        <script type="text/javascript" src="https://cdn.rawgit.com/d3/d3-plugins/master/jsonp/jsonp.js"></script>
        <script type="text/javascript" src="https://rawgit.com/ConstantinoSchillebeeckx/phylogram_d3/master/js/phylogram_d3.js"></script>
        <script type="text/javascript" src="https://rawgit.com/ConstantinoSchillebeeckx/phylogram_d3/master/js/q2_phylogram.js"></script> <!-- must be called after phylogram_d3.js because it will replace the init() function for use in cross-origin -->
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
def make_d3_phylogram(output_dir: str, tree: skbio.TreeNode, otu_metadata: qiime.Metadata) -> None:

    mapping_df = otu_metadata.to_dataframe()

    # ERROR CHECK INPUTS
    if isinstance(mapping_df, pd.DataFrame):

        leaves = set([l for l in tree.traverse() if l.is_tip()])
        mapping_otus = set(mapping_df.index)

        if leaves > mapping_otus:
            print("\n*** NOTE *** ")
            print("Not all leaves were found in the OTU mapping file; as a consequence, these leaves cannot be styled.\n")


    # CONSTRUCT BODY TAG
    dat_tree = '"dat/tree.tre"'
    div = '"#phylogram"'
    dat_mapping = '{"mapping_dat" : %s}' %mapping_df.reset_index().to_json(orient="records") # store the mapping file in the options obj
    if isinstance(mapping_df, pd.DataFrame):
        body = "\t<body onload='init(%s, %s, %s);'>" %(dat_tree, div, dat_mapping)
    else:
        body = "\t<body onload='init(%s, %s);'>" %(dat_tree, div)

    index = template.replace('REPLACE',body) # html to write to index.html


    # WRITE ALL OUR FILES
    # index.html, tree.tre, mapping.txt (optional)
    dat_dir = os.path.join(output_dir,'dat')
    if not os.path.exists(dat_dir):
        os.makedirs(dat_dir)
    with open(os.path.join(output_dir,'index.html'), 'w') as fout:
        fout.write(index)
    tree_out = os.path.join(dat_dir,'tree.tre')
    with open(tree_out, 'w') as fout:
        fout.write("d3.jsonp.readNewick('%s');" %str(tree).strip()) # add callback around Newick string for use in cross-origin setting




plugin = Plugin(
    name='phylogram',
    version=__version__,
    website='https://github.com/ConstantinoSchillebeeckx/q2-phylogram',
    package='q2_phylogram'
)

plugin.visualizers.register_function(
    function=make_d3_phylogram,
    inputs={'tree': Phylogeny},
    parameters={'otu_metadata': qiime.plugin.Metadata},
    name='Visualize phylogram',
    description='Generate interactive visualization of your phylogenetic tree.'
)

def tree_to_skbio_tree(data_dir):
    with open(os.path.join(data_dir, 'tree.nwk'), 'r') as fh:
        return skbio.io.read(fh, format="newick", into=skbio.TreeNode)

plugin.register_data_layout_reader('tree', 1, skbio.TreeNode, tree_to_skbio_tree)
