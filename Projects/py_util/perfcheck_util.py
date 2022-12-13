import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import product
import sklearn

def plot_confusion_matrix(clf, X, y):
    """This function is used to plot Confusion Matrix.

    Parameters
    ----------
    clf: scikit-learn classification estimator object
       The estimator of the classification method
    X: pandas.DataFrame, ndarray 
       Feature dataset
    y: pandas.series, array
       Target variable
   
    Results
    -------
    None
    """

    y_pred = clf.predict(X)
    cm = sklearn.metrics.confusion_matrix(y,y_pred)
    fig, ax = plt.subplots(figsize=(5, 5))
    n_classes = cm.shape[0]
    im_ = ax.imshow(cm, interpolation='nearest', cmap='GnBu', alpha=0.8)
    cmap_min, cmap_max = im_.cmap(0), im_.cmap(256)
    text_ = np.empty_like(cm, dtype=object)
    # print text with appropriate color depending on background
    thresh = (cm.max() + cm.min()) / 2.0
    for i, j in product(range(n_classes), range(n_classes)):
        color = cmap_max if cm[i, j] < thresh else cmap_min
        text_cm = format(cm[i, j], '.2g')
        if cm.dtype.kind != 'f':
            text_d = format(cm[i, j], 'd')
            if len(text_d) < len(text_cm):
                text_cm = text_d
        text_[i, j] = ax.text(j, i, text_cm, ha="center", va="center",color=color)
        
    display_labels = np.arange(n_classes)
    fig.colorbar(im_, ax=ax)
    ax.set(xticks=np.arange(n_classes),
           yticks=np.arange(n_classes),
           xticklabels=display_labels,
           yticklabels=display_labels,
           ylabel="True label",
           xlabel="Predicted label")

    ax.set_ylim((n_classes - 0.5, -0.5))
    ax.set_title('confusion matrix')
    plt.setp(ax.get_xticklabels(), rotation='horizontal')
    plt.show()


def plot_feature_importance(estimator, feature_names, encode_cat_list, figsize=(8, 8)):
    """
    The function is used to plot the feature importance from most important to least
    for logistic regresssion and tree-based method: random forest, bagging, boosting.
    Logistic Regression: Feature importance is using the absolute value of the coefficient (Condition on that the dataset is standardized)
    Tree-based Methods: Feature importance is based on the 
    If there are one-hot encoding categorical variables, the plot will group these variables together.
    
    Parameters
    ----------
    estimator: A fitted scikit-learn estimator object
    features_names: array
                    Feature names of the dataset
    """
    if type(estimator) == type(sklearn.linear_model.LogisticRegression()):
        importance_array = estimator.coef_.reshape(-1)
    else:
        importance_array = estimator.feature_importances_.reshape(-1)
    
    importance_df = pd.DataFrame({'var_name_lvl2':np.array(feature_names), 'import_v': importance_array})
    # identify the encoding categorical variables
    importance_df['var_name_lvl1'] = np.where(importance_df['var_name_lvl2'].str.split('_').str[0].isin(encode_cat_list), 
    importance_df['var_name_lvl2'].str.split('_').str[0], importance_df['var_name_lvl2'])
    importance_df['import_v_abs'] = np.abs(importance_df['import_v'])
    import_abs_max = importance_df.groupby('var_name_lvl1', as_index=False)['import_v_abs'].max().rename(columns={'import_v_abs': 'import_v_abs_max'})
    importance_df = importance_df.merge(import_abs_max, on='var_name_lvl1')
    importance_df['color'] = np.where(importance_df['import_v'] < 0, '#CE7777', 'steelblue')
    importance_df_plot = importance_df.sort_values(by=['import_v_abs_max', 'import_v_abs'], ascending=False)
    # Create Figure
    fig, ax = plt.subplots(figsize=figsize)
    pos = np.arange(len(importance_array)) + 0.5
    ax.barh(y=pos, width=importance_df_plot['import_v_abs'], color=importance_df_plot['color'], align="center")
    ax.set_yticks(pos, importance_df_plot['var_name_lvl2'])
    ax.set_title('Feature Importance')
    plt.show()