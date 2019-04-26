#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: KSchoenberger1
"""

from binance_api import Binance
import os
import datetime
import calendar
import numpy as np
import pandas as pd
import copy
import json
import time
import requests
from scipy.stats import rankdata

# In[]:

class binance_kline_info:

    # (str) symbol:
    def __init__(self, account_name, symbol, interval_str,
                 api_key, api_secret):

        self.account_name = account_name
        self.symbol = symbol
        self.interval_str = interval_str

        self.interval = self.count_seconds(self.interval_str)

        self.host = 'https://api.binance.com'
        self.api_key = api_key
        self.api_secret = api_secret

            # build binance api connection:
        self.binance_con = Binance(self.host, self.api_key, self.api_secret)

    # (str) interval_str:
    def count_seconds(self, interval_str):

            # convert interval_str to intervals of seconds:
        interval = int(interval_str[ : (-1)])
        if interval_str[-1] == 'm':
            interval = interval * 60
        elif interval_str[-1] == 'h':
            interval = interval * 60 * 60
        elif interval_str[-1] == 'd':
            interval = interval * 60 * 60 * 24
        elif interval_str[-1] == 'w':
            interval = interval * 60 * 60 * 24 * 7
        elif interval_str[-1] == 'M':
            interval = interval * 60 * 60 * 24 * 30

        self.interval = interval

        return interval

    def count_minutes(self, interval_str):

        minutes = int(self.count_seconds(interval_str) / 60)

        return minutes

    # (str) interval_str: kline frequency: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    # (datetime) startTime_str
    # (datetime) endTime_str
    def count_periods(self, startTime_str, endTime_str):

            # convert startTime_str and endTime_str to float (millisecond):
        startTime = calendar.timegm(startTime_str.timetuple()) * 1000
        endTime = calendar.timegm(endTime_str.timetuple()) * 1000

             # every kline_info includes up to 500 rows (one period),
        total_periods = int((endTime - (startTime - 1)) / (500 * 1000 * self.interval)) + 1

        return (startTime, endTime, total_periods)

    # get_kline_info:
        # (pd.dataframe) kline_info
    def get_kline_info(self, startTime, endTime, total_periods):

        temp_str = 'Step 1.1 Getting kline info data: '
        print (temp_str)

        kline_info_columns = ['open_time', 'momentum_time', 'Open', 'High', 'Low', 'Close', 'volume',
                              'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume',
                              'taker_buy_quote_asset_volume']

        kline_info = pd.DataFrame(columns = kline_info_columns)

        for k in range(0, total_periods):

            curr_startTime = startTime + self.interval * k * 500 * 1000
            curr_endTime = curr_startTime + self.interval * 500 * 1000

            if curr_endTime > endTime:
                curr_endTime = endTime

            sub_kline_info = self.binance_con.kline(self.symbol, self.interval_str, 0, curr_startTime, curr_endTime)

            if kline_info.shape[0] == 0:
                kline_info = sub_kline_info
            else:
                kline_info = kline_info.append(sub_kline_info)

        return kline_info

    def test_data_completeness(self, kline_info, interval):

        temp_str = 'Step 1.2 Testing data completeness: '
        print (temp_str)

        open_time = kline_info['open_time'].values

        for k in range(1, open_time.shape[0]):
            prev_time = open_time[k - 1]
            curr_time = open_time[k]
            if ((curr_time - prev_time) != (interval * 1000)):
                temp_str = str(k) + ': ' + str(prev_time) + ', ' + str(curr_time)
                print (temp_str)

    def adjust_open_close_time(self, kline_info, interval):

        temp_str = 'Step 1.3 Adjusting open and close time: '
        print (temp_str)

        open_time = kline_info['open_time'].values
        open_time = (open_time / (interval * 1000)).astype('int') * interval * 1000
        close_time = open_time + interval * 1000 - 1

        kline_info['open_time'] = open_time
        kline_info['close_time'] = close_time

        return kline_info

    # save_data: save kline_info to csv file:
    def save_kline_info(self):

        temp_str = 'Step 1.4 Saving kline info data to csv files: '
        print (temp_str)

        file_name = os.getcwd() + '/kline_data/binance-' + self.symbol + '-' + self.interval_str + '.csv'
        self.kline_info.to_csv(file_name)

    # unique_data: find the corresponding row in kline_info by 'open_time':
    def unique_data(self, kline_info):

        unique_index = np.arange(0, kline_info.shape[0])
        for k in range(1, unique_index.shape[0]):
            prev_time = kline_info.iloc[k - 1]['open_time']
            curr_time = kline_info.iloc[k]['open_time']
            if (prev_time == curr_time):
                unique_index = unique_index[unique_index != k]

        kline_info = kline_info.iloc[unique_index]

        return kline_info

    # read_kline_info: read the kline data from the csv file:
    def read_kline_info(self):

        file_name = os.getcwd() + '/kline_data/binance-' + self.symbol + '-' + self.interval_str + '.csv'
        kline_info = pd.read_csv(file_name, index_col = 0)

        return kline_info

    # update_kline_info: update the kline_info data to endTime_str:
    def update_kline_info(self, kline_info, endTime_str):

        startTime = int(kline_info.iloc[-1]['close_time'] + 1)
        endTime = calendar.timegm(endTime_str.timetuple()) * 1000

        total_periods = int((endTime - (startTime - 1)) / (500 * 1000 * self.interval)) + 1

        new_kline_info = self.get_kline_info(startTime, endTime, total_periods)

        kline_info = kline_info.append(new_kline_info)

        return kline_info
