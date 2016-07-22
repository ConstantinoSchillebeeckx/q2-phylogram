# q2-phylogram
QIIME2 plugin for generating interactive [D3.js based phylograms](https://github.com/ConstantinoSchillebeeckx/phylogram_d3)

Installing: ```pip install https://github.com/ConstantinoSchillebeeckx/q2-phylogram/archive/master.zip```

## Usage

Convert input Newick tree to QIIME2 artifact:

```qiime tools import --type Phylogeny --input-path demo/tree.tre --output-path tree.qza```

Generate visualization:

```qiime phylogram make-d3-phylogram --i-tree tree.qza --m-otu-metadata-file demo/mapping.txt --o-visualization viz.qzv```

View visualization:

```qiime tools view viz.qzv```
