# Clustering Grids

This small tutorial will show how to use Gridtest to generate grids to run the
[scikit-learn](https://scikit-learn.org/stable/auto_examples/cluster/plot_linkage_comparison.html#sphx-glr-auto-examples-cluster-plot-linkage-comparison-py) cluster plot linkage comparison.
There are three parts:

## Dataset and Algorithms Grids

[1-dataset-algorithms-grids](1-dataset-algorithms-grids/) walks through
converting the original script to have functions that populate dataset and
algorithms grids that are parameterized to run over a single function
to plot one dataset. This example serves to show the basic steps and thinking
to convert a top to bottom script to a simple grid design.

## Modular Grids

[2-modular-grids](2-modular-grids) takes the original design, and improves
upon it by making the datasets and algorithms completely modular, meaning
that we can run each dataset/algorithm combination as a separate task, and
add metrics to compare performance.

