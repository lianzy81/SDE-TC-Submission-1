import numpy as np
import pandas as pd

def show_unique_values(df, exclude_list=[]):
    """ Show unique values in each column of input data.

    Args:
        df (pandas dataframe): input data with the required columns to show unique values.
        exclude_list (list): column names to exclude from showing unique values
    """
    for col in df.columns:
        if col in exclude_list:
            continue
        print('{}: {} unique values.\n{}\n'.format(col, len(df[col].unique()), df[col].unique()))

def custom_ordinal_encoder(df, ordinal_columns, value_dict):
    """Encodes ordinal columns based on custom category-value mappings.

    If there are missing categories, the median ordinal value will be filled in.

    Args:
        df (pandas dataframe): that only contains columns to be encoded as ordinal.
        ordinal_columns (list): names of categorical columns to be converted to ordinal values.
        value_dict (dictionary): mapping of categories to values for each ordinal column.

    Returns:
        pandas dataframe: with ordinal columns encoded as ordinal values.
    """   
    for col in ordinal_columns:
        median_value = int(np.median([i for i in value_dict[col].values()]))
        df[col] = df[col].map(value_dict[col]).fillna(median_value)
    return df

def custom_onehot_encoder(df, onehot_columns, prefix_sep='_'):       
    dummy_df = pd.get_dummies(df[onehot_columns], prefix=onehot_columns, prefix_sep=prefix_sep)
    return pd.concat([df, dummy_df], axis=1)