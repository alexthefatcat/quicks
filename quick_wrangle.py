# -*- coding: utf-8 -*-
"""Created on Fri Nov  3 18:41:34 2023@author: alexm"""

def typeify_columns(df):
    df = df.copy()
    for col in df.columns:
        if '(int)' in  col:
            df[col] = df[col].astype(int)
            df = df.rename(columns={col:col.replace('(int)', '')})
        if '(float)' in  col:
            df[col] = df[col].astype(float)
            df = df.rename(columns={col:col.replace('(float)', '')})
    return df