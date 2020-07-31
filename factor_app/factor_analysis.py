"""
    factor analysis for each asset class
    
"""
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# index name
# STOCK_LIST = [
#     ['SP500', '^GSPC'],  # US
#     # ['FTSE', '^FTSE'],  # UK (not available...)
#     ['GDAXI', '^GDAXI'],  # Germany
#     ['N225', '^N225'],  # Japan
#     ['HSI', '^HSI'],  # Hong Kong
#     ['AORD', '^AORD'],  # Australia
# ]
STOCK_LIST = [
    ['国内株式', '1475.T'],
    ['先進国株式', '1657.T'],
    ['新興国株式', '1658.T'],
]
CURR_LIST = [
    ['USDJPY', 'JPY=X'],
    ['EURJPY', 'EURJPY=X'],
    ['GBPJPY', 'GBPJPY=X'],
]
# TERM_LIST = [
#     ['DGS10', 'DGS5', 'DGS2', 'DGS1MO', 'DGS3MO'],
#     ['10yr', '5yr', '2yr', '1m', '3m'],
# ]
TERM_LIST = [
    ['国内債券', '2510.T'],
    ['先進国債券', '1656.T'],
    ['新興国債券', '2519.T'],
]


def get_return(df):
    df = df.fillna(method='ffill')
    df = df.dropna()
    df = df.pct_change().mean(axis=1)
    return df


def get_factor_return(is_cum_index=False, num_of_days=7):
    date_start = datetime.today() - timedelta(days=num_of_days)
    date_end = datetime.today()

    # 株式
    stock_data = pd.DataFrame()
    for elem in STOCK_LIST:
        stock_data[elem[0]] = pdr.DataReader(
            elem[1], 'yahoo', date_start, date_end)['Close']
    stock_data = get_return(stock_data)

    # 為替
    # https://cartman0.hatenablog.com/entry/2017/11/12/pandas%E3%81%A7%E7%82%BA%E6%9B%BF%E3%83%87%E3%83%BC%E3%82%BFUSD/JPY%E3%81%AE%E5%8F%96%E5%BE%97
    curr_data = pd.DataFrame()
    for elem in CURR_LIST:
        curr_data[elem[0]] = pdr.DataReader(
            elem[1], 'yahoo', date_start, date_end)['Close']
    curr_data = get_return(curr_data)

    # 金利
    # # FREDの金利データは速報性がなかったため採用せず
    # # https://stackoverflow.com/questions/44751510/matplotlib-us-treasury-yield-curve
    # yield_data = pdr.DataReader(TERM_LIST[0], 'fred', date_start, date_end)
    # names = dict(zip(TERM_LIST[0], TERM_LIST[1]))
    # yield_data = yield_data.rename(columns=names)
    # # yield_data = yield_data.rename(columns=names)[['3m']]
    # yield_data = yield_data.fillna(method='ffill')
    # yield_data = yield_data - yield_data.shift(1)
    # yield_data = yield_data.mean(axis=1)

    # 金利
    # 債券系ETF
    yield_data = pd.DataFrame()
    for elem in TERM_LIST:
        yield_data[elem[0]] = pdr.DataReader(
            elem[1], 'yahoo', date_start, date_end)['Close']
    yield_data = get_return(yield_data)

    # データまとめ
    return_data = pd.concat(
        [stock_data, curr_data, yield_data], axis=1, join='inner')
    names = dict(zip(return_data.columns, ['株式ファクター', '為替ファクター', '金利ファクター']))
    return_data = return_data.rename(columns=names)

    if is_cum_index:
        # 下記の実装だと表示データ数が1つ少なくなる点に注意
        return_data.iloc[0] = np.zeros(return_data.shape[1])
        cum_return = 100 * (1 + return_data).cumprod()
        cum_return = cum_return.fillna(method='ffill')
        cum_return = cum_return.dropna()
        return cum_return
    else:
        return_data = return_data.dropna()
        return return_data


def get_asset_return(is_cum_index=False, num_of_days=7):
    # インデックスデータの代理変数としてETF終値を使用（配当の調整はやってない）
    # 国内債券・新興国債券はNEXT FUNDS、他はiシェアーズで代理
    # iシェアーズ: https://www.blackrock.com/jp/individual/ja/strategies/ishares-tse
    # JPX: https://www.jpx.co.jp/equities/products/etfs/issues/01-09.html
    ASSET_LIST = [
        ['国内債券', '2510.T'],
        ['国内株式', '1475.T'],
        ['先進国債券', '1656.T'],
        ['先進国株式', '1657.T'],
        ['新興国債券', '2519.T'],
        ['新興国株式', '1658.T'],
        ['国内リート', '1476.T'],
        ['先進国リート', '1659.T'],
    ]
    date_start = datetime.today() - timedelta(days=num_of_days)
    date_end = datetime.today()

    asset_data = pd.DataFrame()
    for elem in ASSET_LIST:
        asset_data[elem[0]] = pdr.DataReader(
            elem[1], 'yahoo', date_start, date_end)['Close']
    asset_data = asset_data.fillna(method='ffill')
    asset_data = asset_data.dropna()

    # 100スタートのインデックスにして表示してみる
    asset_return = asset_data.pct_change()
    asset_return = asset_return.dropna()
    asset_return.fillna(0, inplace=True)

    if is_cum_index:
        # 下記の実装だと表示データ数が1つ少なくなる点に注意
        asset_return.iloc[0] = np.zeros(asset_return.shape[1])
        cum_return = 100 * (1 + asset_return).cumprod()
        cum_return = cum_return.fillna(method='ffill')
        cum_return = cum_return.dropna()
        return cum_return
    else:
        asset_return = asset_return.dropna()
        return asset_return


def get_factor_analysis():
    result = pd.DataFrame()

    # データ準備
    factor_return = get_factor_return(num_of_days=365)
    asset_return = get_asset_return(num_of_days=365)
    factor_names = factor_return.columns
    asset_names = asset_return.columns
    data = pd.concat([factor_return, asset_return], axis=1, join='inner')

    x = data[factor_names]
    for asset_name in asset_names:
        y = data[asset_name]
        model = LinearRegression(fit_intercept=False)
        model.fit(x, y)

        y_hat = model.predict(x.tail(2).head(1))
        x_hat = model.coef_ * x.tail(2).head(1)
        x_hat['その他'] = y.tail(2).head(1) - y_hat
        result[asset_name] = x_hat.values[0]

    result = result.rename(index=dict(zip(result.index, x_hat.columns)))
    result = result.transpose()
    date = x_hat.index[0]
    # date = str(x_hat.index.values[0])[:10]
    return result, date
