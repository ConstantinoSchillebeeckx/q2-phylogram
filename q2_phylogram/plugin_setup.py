# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import importlib

import qiime.plugin

from q2_phylogram import __version__

plugin = qiime.plugin.Plugin(
    name='phylogram',
    version=__version__,
    website='https://github.com/ConstantinoSchillebeeckx/q2-phylogram',
    package='q2_phylogram'
)

importlib.import_module('q2_types.make_d3_phylogram')
