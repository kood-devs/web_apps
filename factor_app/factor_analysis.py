"""
    factor analysis for each asset class
    
"""
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
from keras import models, layers

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# CONST
TRAIN_START = datetime(1990, 1, 1)
TRAIN_END = datetime.today()
EPOCH = 50
BATCH_SIZE = 128

EXCHANGES = [
    ['SP500', '^GSPC'],  # US
    # ['FTSE', '^FTSE'],  # UK FTSE100
    ['FTSE', '^FTAI'],  # UK FTSE250
    ['GDAXI', '^GDAXI'],  # Germany
    ['N225', '^N225'],  # Japan
    ['HSI', '^HSI'],  # Hong Kong
    ['AORD', '^AORD'],  # Australia
]

# 株式
close_price = pd.DataFrame()
date_start = datetime.today() - timedelta(weeks=1)
date_end = datetime.today()
for name in EXCHANGES:
    close_price[name[0]] = pdr.DataReader(
        name[1], 'yahoo', date_start, date_end)['Close']
close_price = close_price.fillna(method='ffill')
close_price = close_price.round(2)

# 為替
# https://cartman0.hatenablog.com/entry/2017/11/12/pandas%E3%81%A7%E7%82%BA%E6%9B%BF%E3%83%87%E3%83%BC%E3%82%BFUSD/JPY%E3%81%AE%E5%8F%96%E5%BE%97
JPY_USD = pdr.DataReader('JPY=X', 'yahoo', date_start, date_end)
JPY_EUR = pdr.DataReader('EURJPY=X', 'yahoo', date_start, date_end)
JPY_GBP = pdr.DataReader('GBPJPY=X', 'yahoo', date_start, date_end)

# 金利
# FF three-factor
# ip = pdr.DataReader("F-F_Research_Data_Factors", "famafrench")
