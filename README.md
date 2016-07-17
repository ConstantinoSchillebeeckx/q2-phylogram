# q2-phylogram
QIIME2 plugin for generating interactive [D3.js based phylograms](https://github.com/ConstantinoSchillebeeckx/phylogram_d3)

Installing: ```pip install https://github.com/ConstantinoSchillebeeckx/q2-phylogram/archive/master.zip```

## Usage

Convert input Newick tree to QIIME2 artifact
```qiime tools import --type Phylogeny --input-path example/tree.tre --output-path tree.qza```

Generate visualization
```qiime phylogram make_d3_phylogram --tree tree.qza --otu-metadata-file example/mapping.txt --visualization viz.qzv```
