# Examples

## Grids

GridTest can be used just to generate grids that are useful for however you please! For example, we can define
and then load a grids.yml file in our Python code to parameterize tests or other functions.

 - [grids](grids): is an example of defining different grids for your use in a grids.yml file.

## Testing

 - [basic](basic): shows writing a grid test file for a basic script
 - [read-write](read-write): shows how to use template substitutes `{% tmp_path %}` and `{% tmp_dir %}` for creating temporary files and directories for tests.
 - [is-true-false](is-true-false): example tests for using the `istrue` and `isfalse` conditions.
 - [package](package): generate for a python package you've already installed
 - [class](class): run grid tests for a car class

## Metric Collection

 - [metrics](metrics): use decorators to measure metrics across a grid of tests (eg., timeit)
 - [custom-decorator](custom-decorator): writing a custom decorator to count words over a grid of parameters
 - [grid-function](grid-function) gridtest can derive input parameters from one or more functions.


## Grids

 - [grids](grids): an introduction to generating and using grids.
 - [clustering-grids](clustering-grids): using GridTest to easily run the [clustering example for scikit-learn](https://scikit-learn.org/stable/auto_examples/cluster/plot_linkage_comparison.html#sphx-glr-auto-examples-cluster-plot-linkage-comparison-py)

Also see the [tutorials](https://vsoch.github.io/gridtest/tutorials/) section of the web documentation for more details.
