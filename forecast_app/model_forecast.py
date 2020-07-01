"""
    Google (2015)
    URL: https://github.com/corrieelston/datalab/blob/master/FinancialTimeSeriesTensorFlow.ipynb
"""
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense

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
    ['NYSE', '^NYA'],  # US
    ['DOW', '^DJI'],  # US
    ['NASDAQ', '^IXIC'],  # US
    # ['FTSE', '^FTSE'],  # UK...現在は取得できず
    ['GDAXI', '^GDAXI'],  # Germany
    ['N225', '^N225'],  # Japan
    ['HSI', '^HSI'],  # Hong Kong
    ['AORD', '^AORD'],  # Australia
]

MODEL_LIST = [
    "DNN",
    "binomial logit",
    "SVC",
    "kernel SVC",
    "decision tree",
]


def get_recent_index(num_week=2):
    # 終値を取得
    close_price = pd.DataFrame()
    date_start = datetime.today() - timedelta(weeks=num_week)
    date_end = datetime.today()
    for name in EXCHANGES:
        close_price[name[0]] = pdr.DataReader(
            name[1], 'yahoo', date_start, date_end)['Close']
    close_price = close_price.fillna(method='ffill')
    close_price = close_price.dropna()
    close_price = close_price.round(2)
    return close_price


def get_return(start_date, end_date, index_list, data_length, number_of_shift=3):
    # 終値を取得
    close_price = pd.DataFrame()
    for name in index_list:
        close_price[name[0]] = pdr.DataReader(
            name[1], 'yahoo', start_date, end_date)['Close']
    close_price = close_price.fillna(method='ffill')  # 休場日は前日終値を横置き
    # close_price = close_price.dropna()  # 休場日は除外
    # close_price.to_csv('index.csv')  # 一応データを保存しておく

    # 算術リターンに変換
    close_return = pd.DataFrame()
    for name in index_list:
        close_return[name[0] + '_ret'] = close_price[name[0]] / \
            close_price[name[0]].shift(1) - 1
    close_return = close_return[close_return['N225_ret'] != 0]  # 日本市場が休場の場合は削除

    # 差分データを準備
    train_data = pd.DataFrame()
    train_data['N225_ret_pos'] = (close_return['N225_ret'] > 0) * 1
    for col_name in close_return:
        for i in range(number_of_shift):
            train_data[col_name +
                       str(i + 1)] = close_return[col_name].shift(i + 1)

    # テストデータを準備
    test_data = pd.DataFrame()
    for col_name in close_return:
        for i in range(number_of_shift):
            test_data[col_name +
                      str(i)] = close_return[col_name].shift(i)

    # 型を整えてデータを返却
    train_data = train_data.dropna()
    train_data.tail(data_length)
    # train_data.to_csv(
    #     'learn_data_{}.csv'.format(number_of_shift))
    x_val = np.array(train_data.iloc[:, 1:])
    y_val = np.array(train_data.iloc[:, 0]).reshape(-1)
    return x_val, y_val, test_data.tail(1)


def learn_model(model_type, x_train, y_train):
    """
    指定した学習器を使用してモデルを構築して
    訓練データにおける正答率と共に学習済みのモデルを返す関数
    """
    if model_type == "DNN":  # DNN
        # モデル構成
        model = Sequential()
        model.add(Dense(32, activation='relu',
                        input_shape=(x_train.shape[1],)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam',
                      loss='binary_crossentropy', metrics=['accuracy'])
        model.fit(x_train, y_train, epochs=EPOCH, batch_size=BATCH_SIZE)
        # 正答率
        acc = sum(
            [1 if val >= 0.5 else 0 for val in model.predict(x_train)] == y_train)
        acc /= y_train.shape[0]
        return model, acc

    # RNNは若干インプットを調整する必要あり
    # elif model_type == "RNN":  # RNN
    #     # モデル構成
    #     model = models.Sequential()
    #     model.add(layers.LSTM(32, batch_input_shape=(
    #         None, x_train.shape[1], x_train.shape[2]), activation='relu'))
    #     model.add(layers.Dense(32, activation='relu'))
    #     model.add(layers.Dense(1, activation='sigmoid'))
    #     model.compile(optimizer='rmsprop',
    #                   loss='binary_crossentropy', metrics=['accuracy'])
    #     model.fit(x_train, y_train, epochs=EPOCH, batch_size=BATCH_SIZE)
    #     # 正答率
    #     acc = sum(
    #         [1 if val >= 0.5 else 0 for val in model.predict(x_train)] == y_train)
    #     acc /= y_train.shape[0]
    #     return model, acc

    elif model_type == "binomial logit":  # 二項ロジット
        # モデル構成
        model = LogisticRegression(penalty='none', max_iter=1e10, tol=1e-10)
        model.fit(x_train, y_train)
        # 正答率
        acc = sum(model.predict(x_train) == y_train) / y_train.shape[0]
        return model, acc

    elif model_type == "SVC":  # 線形SVC
        # モデル構成
        model = SVC(kernel='linear', random_state=1, C=1.0)
        model.fit(x_train, y_train)
        # 正答率
        acc = sum(model.predict(x_train) == y_train) / y_train.shape[0]
        return model, acc

    elif model_type == "kernel SVC":  # カーネルSVC
        # モデル構成
        model = SVC(kernel='rbf', random_state=1, gamma=100.0, C=1.0)
        model.fit(x_train, y_train)
        # 正答率
        acc = sum(model.predict(x_train) == y_train) / y_train.shape[0]
        return model, acc

    elif model_type == "decision tree":  # 決定木
        # モデル構成
        model = DecisionTreeClassifier(
            criterion='gini', max_depth=4, random_state=1)
        model.fit(x_train, y_train)
        # 正答率
        acc = sum(model.predict(x_train) == y_train) / y_train.shape[0]
        return model, acc

    else:
        raise ValueError("Incorrect input")


def run_forecast(asset_class, forecast_model, train_num):
    # データを準備
    x_train, y_train, x_test = get_return(
        TRAIN_START, TRAIN_END, EXCHANGES, train_num)
    prediction_date = x_test.index[0]

    # TODO: 祝日の影響を正しく反映する
    if prediction_date.weekday() == 4:
        prediction_date += pd.offsets.Day(2)
    prediction_date += pd.offsets.Day(1)
    # prediction_date = prediction_date.strftime('%Y/%m/%d')

    # 学習を実施・結果を出力
    model, acc = learn_model(forecast_model, x_train, y_train)
    result = model.predict(np.array(x_test))
    return prediction_date, result
