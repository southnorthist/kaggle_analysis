import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def split_num_cat_target(df, id, target, lvl_theta):
    categorical_col = df.nunique()[df.unique() <= lvl_theta].keys().to_list()
    target_col = df[target]
    id_col = df[id]
    numeric_col = [col for col in df.columns if col not in categorical_col + target_col + id_col]
    return {'categorical': categorical_col, 'target': target_col, 'id': id_col, 'numerical': numeric_col}

def plot_all_dist(df, figsize, num_var, row, col):
    plt.style.use('ggplot2')
    fig = plt.figure(figsize = figsize)
    for index in range(1, len(num_var) + 1):
        ax = fig.add_subplot(row, col, index)
        ax.hist(df[num_var[index-1]], bins = 50, color = 'steelblue', alpha = 0.7)
        ax.set_title(num_var[index - 1])
        plt.subplots_adjust(left=0.1,
                            bottom=0.1,
                            right=0.9,
                            top=0.9,
                            wspace=0.4,
                            hspace=0.4)
    plt.show()
    
