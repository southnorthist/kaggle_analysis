import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def split_num_cat_target(df, target, id=None, lvl_theta=10):
    if id != None:
        id_col = df[id]
    else:
        id_col = []
    target_col = [target]
    df_X =  df.drop(columns = target_col)
    categorical_col = df_X.nunique()[df_X.nunique() <= lvl_theta].keys().to_list()
    numeric_col = [col for col in df.columns if col not in categorical_col + target_col + id_col]
    return {'categorical': categorical_col, 'target': target_col, 'id': id_col, 'numeric': numeric_col}

def plot_all_dist(df, figsize, num_var, row, col):
    #plt.style.use('ggplot2')
    fig = plt.figure(figsize = figsize)
    for index in range(1, len(num_var) + 1):
        ax = fig.add_subplot(row, col, index)
        ax.hist(df[num_var[index-1]], bins = 50, color = 'steelblue', alpha = 0.7)
        ax.set_title(num_var[index - 1])
        plt.subplots_adjust(left=0.1,
                            bottom=0.05,
                            right=0.9,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)
    plt.show()

def add_value_labels(ax, spacing=5, fmt="{:.1f}", fontsize=8):

    # For each bar: Place a label
        for rect in ax.patches:
            # Get X and Y placement of label from rect.
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2

            # Number of points between bar and label. Change to your liking.
            space = spacing
            # Vertical alignment for positive values
            va = 'bottom'

            # If value of bar is negative: Place label below bar
            if y_value < 0:
                # Invert space to place label below
                space *= -1
                # Vertically align label at top
                va = 'top'

            # Use Y value as label and format number with one decimal place
            label = fmt.format(y_value)

            # Create annotation
            ax.annotate(
                label,                      # Use `label` as label
                (x_value, y_value),         # Place label at end of the bar
                xytext=(0, space),          # Vertically shift label by `space`
                textcoords="offset points", # Interpret `xytext` as offset in points
                ha='center',                # Horizontally center label
                va=va,                      # Vertically align label differently for positive and negative values.
                fontsize=fontsize)          # Specify the font size

def plot_all_freq(df, figsize, cat_var, row, col, **kwargs):
    #plt.style.use('ggplot2')
    fig = plt.figure(figsize = figsize)
    for index in range(1, len(cat_var) + 1):
        ax = fig.add_subplot(row, col, index)
        temp_data = df[cat_var[index-1]].value_counts()
        x = temp_data.index.values
        height = temp_data.values
        ax.bar(x=x, height=height, color = 'steelblue', alpha = 0.7)
        x.sort()
        ax.set_xticks(x)
        ax.set_title(cat_var[index - 1])
        add_value_labels(ax, **kwargs)
        plt.subplots_adjust(left=0.1,
                            bottom=0.05,
                            right=0.9,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)
    plt.show()
    
    
