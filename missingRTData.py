# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 08:12:00 2020

@author: Shawn Leavor
"""

import pandas as pd
import missingno as msno 

df = pd.read_csv('RottenTomatoesScrape/rtData.csv', na_values=[''])
boxOffice = df[df['boxOffice'].notna()]

counts = df.count(0)

msno.matrix(df) 