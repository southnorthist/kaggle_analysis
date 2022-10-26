import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# Elbow Method to Determine the Optimal Number of Clusters
def elbow_curve(X, n_clusters, random_state, plot_curve = True):
    sum_sq_distance = []
    for c in range(1, n_clusters + 1):
        km_c = KMeans(n_clusters = c, init = "k-means++", n_init = 10, max_iter = 300, random_state = random_state).fit(X)
        sum_sq_distance.append(km_c.inertia_)
    if plot_curve == True:
        plt.style.use('ggplot')
        fig, ax = plt.subplots()
        ax.plot(np.arange(1, n_clusters + 1), sum_sq_distance, 'bo-')
        ax.set_xlabel('Number of Clusters')
        ax.set_xticks(np.arange(1, n_clusters + 1))
        ax.set_ylabel('Sum of Squared Distances to Closest Centroids')
        ax.set_title('Elbow Method')
        plt.show()
    return [*zip(range(1, n_clusters + 1), sum_sq_distance)]


# Silhouette Score Method to Determine the Optimal Number of Clusters
def silhouette_curve(X, n_clusters, random_state, plot_curve = True):
    silhouette_score_list = []
    for c in range(2, n_clusters + 1):
        # Number of clusters must start from 2
        km_c = KMeans(n_clusters = c, init = "k-means++", n_init = 10, max_iter = 300, random_state = random_state).fit(X)
        silhouette_score_value = silhouette_score(X, km_c.labels_, metric='euclidean', sample_size=None, random_state=random_state)
        silhouette_score_list.append(silhouette_score_value)
    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    ax.plot(np.arange(2, n_clusters + 1), silhouette_score_list, 'bo-')
    ax.set_xlabel('Number of Clusters')
    ax.set_xticks(np.arange(2, n_clusters + 1))
    ax.set_ylabel('Silhouette Score')
    ax.set_title('Average Silhouette Coefficient')
    plt.show()
    return [*zip(range(2, n_clusters + 1), silhouette_score_list)]


