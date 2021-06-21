"""
Reads a csv containing, for each university, its score for each question
"""

import pandas as pd


# Normalizes columns in df to have values in [0, 1]
def normalize_cols(df):
    result = df.copy()
    for feature_name in df.columns:
        if feature_name != 'university':
            max_value = df[feature_name].max()
            min_value = df[feature_name].min()
            if max_value == min_value:
                result[feature_name] = df[feature_name] / df[feature_name].sum()
            else:
                result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


def parse_csv(filepath):
    df = pd.read_csv(filepath)
    return normalize_cols(df)
