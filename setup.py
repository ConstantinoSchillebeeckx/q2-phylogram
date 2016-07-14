# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages

setup(
    name="q2-phylogram",
    # TODO stop duplicating version string
    version="0.0.0-dev",
    packages=find_packages(),
    install_requires=['qiime >= 2.0.0', 'pandas', 'biopython'],
    author="Constantino Schillebeeckx",
    author_email="constantinoschillebeeckx@gmail.com",
    description="QIIME 2 plugin for generating interactive D3.js based phylogram.",
    license="BSD",
    url="http://www.qiime.org",
    entry_points={
        'qiime.plugins':
        ['q2-phylogram=q2_phylogram.plugin_setup:plugin']
    }
)
