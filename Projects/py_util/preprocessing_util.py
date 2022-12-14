import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from textwrap import wrap
from scipy.stats import chi2_contingency


def split_num_cat_target(df, target, id=None, lvl_theta=10, show=False):
    """
    Given a pandas dataframe, split the columns to be numeric and categorical variables.

    Parameters
    ----------
    df: pandas.DataFrame
    target: str
            Target variable name
    id: str
        ID variable name
    lvl_theta: int
               The threshold level for number of unique values to determine 
               if a variable is a numeric variable or categorical/discrete variable. 
               The default value is 10, i.e., if unique number of values is greater than 10, then it is classified as a numeric variable.
               Otherwise, it is a categorical variable.
    show: boolean
          Whether to show the variables in a tabular format. Default is False.
    Results
    -------
    col_dict: A dictionary that contains the names of categorical, numeric, target, id variables for the dataframe.
    """
    if id != None:
        id_col = df[id]
    else:
        id_col = []
    target_col = [target]
    df_X =  df.drop(columns = target_col)
    categorical_col = df_X.nunique()[df_X.nunique() <= lvl_theta].keys().to_list()
    numeric_col = [col for col in df.columns if col not in categorical_col + target_col + id_col]
    col_dict = {'categorical': categorical_col, 'target': target_col, 'id': id_col, 'numeric': numeric_col}
    if show == True:
        tab_fmt = [['Target', ','.join(target_col)],
                   ['ID', ', '.join(id_col)],
                   ['Numeric', '\n'.join(wrap(', '.join(numeric_col)))], # Wrap text if too many variables
                   ['Categorical', '\n'.join(wrap(', '.join(categorical_col)))]
                  ]
        col_names = ['Type', 'Variables Names']
        print(tabulate(tab_fmt, headers=col_names, tablefmt="fancy_grid"))

    return col_dict

def plot_all_dist(df, figsize, num_var, row, col):
    #plt.style.use('ggplot2')
    fig = plt.figure(figsize = figsize)
    for index in range(1, len(num_var) + 1):
        ax = fig.add_subplot(row, col, index)
        sns.histplot(data=df, x=num_var[index-1], kde= True, alpha=0.7)
        #ax.hist(df[num_var[index-1]], bins = 50, color = 'steelblue', alpha = 0.7)
        ax.set_title(num_var[index - 1])
        plt.subplots_adjust(left=0.1,
                            bottom=0.05,
                            right=0.9,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)
    plt.show()

def add_value_labels(ax, spacing=0.5, fmt="{:.1f}", fontsize=8):

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
        cat_var_name = cat_var[index-1]
        temp_data = df[cat_var_name].value_counts().reset_index()
        #x = temp_data.index.values
        #height = temp_data.values
        sns.barplot(data=temp_data, x='index', y=cat_var_name, color='#277BC0', alpha=0.7)
        #ax.bar(x=x, height=height, color = 'steelblue', alpha = 0.7)
        #x.sort()
        #ax.set_xticks(x)
        ax.set_title(cat_var_name)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        add_value_labels(ax, **kwargs)
        plt.subplots_adjust(left=0.1,
                            bottom=0.05,
                            right=0.9,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)
    plt.show()
    
    
def plot_odds_cat(df, cat_var_list, target, figsize, row, col, **kwargs):
        """
        This function helps to plot the odds ratio for binary classification problem for each category of all the categorical variables.

        Parameters
        ----------
        df: pandas.DataFrame
            The dataframe that is used for the odds ratio plotting
        cat_var_list: list
                      The list of names of all the categorical variables
        target: str
                The target variable name (should be binary)
        figsize: tuple
                 The size of the figure
        row: int
             Number of rows of the figure
        col: int
             Number of cols of the figure
        
        Results
        -------
        None
        """
        fig = plt.figure(figsize = figsize)
        _df = df.copy()
        _df['index'] = df.index.to_series()
        for index in range(1, len(cat_var_list) + 1):
                ax = fig.add_subplot(row, col, index)
                # Calculate odds of the creditability for each category
                cat_var = cat_var_list[index - 1]
                count_df = _df.groupby([cat_var, target], as_index=False)['index'].count().rename(columns={'index':'Count'})
                total_count_df = _df.groupby(cat_var, as_index=False)['index'].count().rename(columns={'index':'Total_Count'})
                perc_df = count_df.merge(total_count_df, on=cat_var)
                perc_df['event_perc'] = perc_df['Count'] / perc_df['Total_Count']
                event = perc_df.loc[perc_df[target] == 1, [cat_var, 'event_perc']].reset_index(drop=True)
                non_event = perc_df.loc[perc_df[target] == 0, [cat_var, 'event_perc']].reset_index(drop=True)
                # Create label 
                cat_label_s = event[cat_var].astype(str)
                count_label_s = total_count_df['Total_Count'].astype(str)
                label_s = cat_label_s.str.cat(count_label_s.str.cat([')']*len(cat_label_s), join='left'), sep='\n(')
                # Create the dataset for plotting
                odds_df = pd.DataFrame({'category':event[cat_var].values, 
                                        'odds': (event['event_perc'] / non_event['event_perc']).values,
                                        'count': total_count_df['Total_Count'],
                                        'label': label_s})
                # Create bar plot
                sns.barplot(data=odds_df, x='category', y='odds', color='#277BC0', alpha=0.7)
                ax.set_title(cat_var)
                add_value_labels(ax, **kwargs)
                ax.tick_params(axis='x', which='major', labelsize=7)
                ax.set_xticklabels(odds_df['label'])
                ax.set_xlabel('category\n(total count)', size=8.5)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)              
                plt.subplots_adjust(left=0.1,
                                bottom=0.05,
                                right=0.9,
                                top=0.95,
                                wspace=0.4,
                                hspace=0.4)
                plt.suptitle('Odds of the Event')
        plt.show()



def cat_var_ind_test(df, cat_var_list):
    chi2_dict = {}
    p_dict = {}
    for i in range(len(cat_var_list)):
        cat_i = cat_var_list[i]
        chi2_dict[cat_i] = []
        p_dict[cat_i] = []
        for j in range(len(cat_var_list)):
            cat_j = cat_var_list[j]
            cross_table = pd.crosstab(df[cat_i], df[cat_j])
            chi2, p, dof, expected = chi2_contingency(cross_table)
            chi2_dict[cat_i].append(chi2)
            p_dict[cat_i].append(p)
    return chi2_dict, p_dict
