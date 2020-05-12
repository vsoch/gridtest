"""
================================================================
Comparing different hierarchical linkage methods on toy datasets
================================================================

This is taken from https://scikit-learn.org/stable/auto_examples/cluster/plot_linkage_comparison.html
and modified for this example

"""
import time
import warnings

import numpy as np
import matplotlib.pyplot as plt

from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler
from itertools import cycle, islice

np.random.seed(0)

######################################################################
# Generate datasets. We choose the size big enough to see the scalability
# of the algorithms, but not too big to avoid too long running times


def generate_datasets(n_samples=1500, factor=0.5, noise=0.05):
    """This generate_datasets function is simply taking the original 
       (top to bottom) style code, and converting into a function to
       return datasets. This function can be provided to a grid, and then
       each dataset will be run across some number of variables to produce
       a grid
    """
    noisy_circles = datasets.make_circles(
        n_samples=n_samples, factor=factor, noise=noise
    )
    noisy_moons = datasets.make_moons(n_samples=n_samples, noise=0.05)
    blobs = datasets.make_blobs(n_samples=n_samples, random_state=8)
    no_structure = np.random.rand(n_samples, 2), None

    # Anisotropicly distributed data
    random_state = 170
    X, y = datasets.make_blobs(n_samples=n_samples, random_state=random_state)
    transformation = [[0.6, -0.6], [-0.4, 0.8]]
    X_aniso = np.dot(X, transformation)
    aniso = (X_aniso, y)

    # blobs with varied variances
    varied = datasets.make_blobs(
        n_samples=n_samples, cluster_std=[1.0, 2.5, 0.5], random_state=random_state
    )

    # name, dataset, params
    return [
        ("circles", noisy_circles, {"n_clusters": 2}),
        ("moons", noisy_moons, {"n_clusters": 2}),
        ("varied", varied, {"n_neighbors": 2}),
        ("aniso", aniso, {"n_neighbors": 2}),
        ("blobs", blobs, {}),
        ("no-structure", no_structure, {}),
    ]


default_base = {"n_neighbors": 10, "n_clusters": 3}


def generate_algorithms(dataset):
    """this was previously in the nested for loop, and returns a tuple of
       algorithms. Since params is derived from a dataset (the index 1) we
       take a dataset as input and then grab the params from it.
    """
    # update parameters with dataset-specific values
    params = default_base.copy()
    params.update(dataset[2])
    ward = cluster.AgglomerativeClustering(
        n_clusters=params["n_clusters"], linkage="ward"
    )
    complete = cluster.AgglomerativeClustering(
        n_clusters=params["n_clusters"], linkage="complete"
    )
    average = cluster.AgglomerativeClustering(
        n_clusters=params["n_clusters"], linkage="average"
    )

    return [
        ("Average Linkage", average),
        ("Complete Linkage", complete),
        ("Ward Linkage", ward),
    ]


def generate_plots(dataset, algorithms, save_prefix="linkage"):
    """Given a dataset and algorithm, generate a plot for each one.
    """
    # unwrap the dataset
    (dataset_name, dataset, algo_params) = dataset

    # Set up cluster parameters
    plt.figure(figsize=(9 * 1.3 + 2, 4.5))
    plt.subplots_adjust(
        left=0.02, right=0.98, bottom=0.001, top=0.96, wspace=0.05, hspace=0.01
    )

    plot_num = 1
    X, y = dataset

    # normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(X)

    for name, algorithm in algorithms:
        t0 = time.time()

        # catch warnings related to kneighbors_graph
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="the number of connected components of the "
                + "connectivity matrix is [0-9]{1,2}"
                + " > 1. Completing it to avoid stopping the tree early.",
                category=UserWarning,
            )
            algorithm.fit(X)

        t1 = time.time()
        if hasattr(algorithm, "labels_"):
            y_pred = algorithm.labels_.astype(np.int)
        else:
            y_pred = algorithm.predict(X)

        plt.subplot(1, len(algorithms), plot_num)
        if plot_num == 1:
            plt.title(dataset_name, size=18)

        colors = np.array(
            list(
                islice(
                    cycle(
                        [
                            "#377eb8",
                            "#ff7f00",
                            "#4daf4a",
                            "#f781bf",
                            "#a65628",
                            "#984ea3",
                            "#999999",
                            "#e41a1c",
                            "#dede00",
                        ]
                    ),
                    int(max(y_pred) + 1),
                )
            )
        )
        plt.scatter(X[:, 0], X[:, 1], s=10, color=colors[y_pred])
        plt.xlim(-2.5, 2.5)
        plt.ylim(-2.5, 2.5)
        plt.xticks(())
        plt.yticks(())
        plt.text(
            0.99,
            0.01,
            ("%.2fs %s" % ((t1 - t0), name)).lstrip("0"),
            transform=plt.gca().transAxes,
            size=15,
            horizontalalignment="right",
        )
        plot_num += 1

    plt.savefig(f"{save_prefix}-{dataset_name}.png")
    plt.close()
