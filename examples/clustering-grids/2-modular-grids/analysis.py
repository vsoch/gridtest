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

    # name, dataset
    return [
        ("circles", noisy_circles),
        ("moons", noisy_moons),
        ("varied", varied),
        ("aniso", aniso),
        ("blobs", blobs),
        ("no-structure", no_structure),
    ]


default_base = {"n_neighbors": 10, "n_clusters": 3}


def generate_algorithms(n_clusters=2):
    """Here we have updated the original generate_algorithms function to separate
       the dataset from it, so it can be run in parallel, and the number of clusters
       variable varied.
    """
    ward = cluster.AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
    complete = cluster.AgglomerativeClustering(
        n_clusters=n_clusters, linkage="complete"
    )
    average = cluster.AgglomerativeClustering(n_clusters=n_clusters, linkage="average")

    return [
        ("Average Linkage", average),
        ("Complete Linkage", complete),
        ("Ward Linkage", ward),
    ]


def generate_plot(dataset, algorithm, save_prefix="linkage"):
    """Given a dataset and algorithm, generate a plot for each one.
    """
    # unwrap the dataset and algorithm
    (dataset_name, dataset) = dataset
    (algorithm_name, algorithm) = algorithm
    X, y = dataset

    # Set up cluster parameters
    plt.figure(figsize=(6, 6))
    plt.subplots_adjust(
        left=0.02, right=0.98, bottom=0.001, top=0.96, wspace=0.05, hspace=0.01
    )

    # normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(X)

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

    if hasattr(algorithm, "labels_"):
        y_pred = algorithm.labels_.astype(np.int)
    else:
        y_pred = algorithm.predict(X)

    plt.subplot(1, 1, 1)
    plt.title(f"{dataset_name} clustered with {algorithm_name}", size=18)

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
    plt.tight_layout()
    output_name = (
        ("%s-%s.png" % (dataset_name, algorithm_name)).replace(" ", "-").lower()
    )
    plt.savefig(output_name)
    plt.close()
