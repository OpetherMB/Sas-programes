#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:41:13 2019

@author: jurado
"""
import pandas as pd
import os

df_ratio_length=pd.read_csv(os.path.dirname(__file__)+"/ratio_road_length")

#print(df_ratio_length)



for column in df_ratio_length.columns :
    if("#" in column):
       df_ratio_length=df_ratio_length.drop(column,axis=1)

df_ratio_length = df_ratio_length.set_index(["angle"])
print(df_ratio_length.columns)
print(df_ratio_length.loc[320.0][0])
#print(df_ratio_length.iloc[6][0])

