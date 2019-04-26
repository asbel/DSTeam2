#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: KSchoenberger1
"""

import pandas as pd
import numpy as np

import json
import requests
import time

class Binance:

    def __init__(self, host, api_key, api_secret):

        self.host = host
        self.api_key = api_key
        self.api_secret = api_secret
        self.s = requests.Session()

    # depth info:
    def depth(self, symbol, limit = 10):

        r = self.s.get('%s/api/v1/depth?symbol=%s&limit=%s' % (self.host, symbol, str(limit)))
        depth_info = json.loads(r.content)

        asks_info = depth_info['asks']
        asks_price = [float(asks_info[k][0]) for k in range(0, len(asks_info))]
        asks_amount = [float(asks_info[k][1]) for k in range(0, len(asks_info))]

        bids_info = depth_info['bids']
        bids_price = [float(bids_info[k][0]) for k in range(0, len(bids_info))]
        bids_amount = [float(bids_info[k][1]) for k in range(0, len(bids_info))]

        depth_info = pd.DataFrame(columns = ['bid_amount', 'bid_price', 'ask_price', 'ask_amount'])
        depth_info['bid_amount'] = bids_amount
        depth_info['bid_price'] = bids_price
        depth_info['ask_price'] = asks_price
        depth_info['ask_amount'] = asks_amount

        return depth_info

    # recent trades:
    def recent_trades(self, symbol, limit = 50):

        r = self.s.get('%s/api/v1/trades?symbol=%s&limit=%s' % (self.host, symbol, str(limit)))
        recent_trades_info = json.loads(r.content)

        trades_id = [recent_trades_info[k]['id'] for k in range(0, len(recent_trades_info))]
        isBestMatch = [recent_trades_info[k]['isBestMatch'] for k in range(0, len(recent_trades_info))]
        isBuyerMaker = [recent_trades_info[k]['isBuyerMaker'] for k in range(0, len(recent_trades_info))]
        price = [recent_trades_info[k]['price'] for k in range(0, len(recent_trades_info))]
        qty = [recent_trades_info[k]['qty'] for k in range(0, len(recent_trades_info))]
        trades_time = [recent_trades_info[k]['time'] for k in range(0, len(recent_trades_info))]

        recent_trades_info = pd.DataFrame(index = trades_time, columns = ['trade_id', 'isBestMatch', 'isBuyerMaker',
                                                                          'price', 'quantity'])
        recent_trades_info['trade_id'] = trades_id
        recent_trades_info['isBestMatch'] = np.array(isBestMatch).astype('int')
        recent_trades_info['isBuyerMaker'] = np.array(isBuyerMaker).astype('int')
        recent_trades_info['price'] = price
        recent_trades_info['quantity'] = qty

        return recent_trades_info

    # get kline info:
    def kline(self, symbol, interval, limit = 0, startTime = 0, endTime = 0):
        # interval can be: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        address = self.host + '/api/v1/klines?symbol=' + symbol + '&interval=' + str(interval)
        if (limit > 0):
            address = address + '&limit=' + str(limit)
        if (startTime > 0 and endTime > 0):
            address = address + '&startTime=' + str(startTime) + '&endTime=' + str(endTime)
        r = self.s.get(address)

        kline_info = json.loads(r.content)

        open_time = [kline_info[k][0] for k in range(0, len(kline_info))]
        open_price = [float(kline_info[k][1]) for k in range(0, len(kline_info))]
        high_price = [float(kline_info[k][2]) for k in range(0, len(kline_info))]
        low_price = [float(kline_info[k][3]) for k in range(0, len(kline_info))]
        close_price = [float(kline_info[k][4]) for k in range(0, len(kline_info))]
        volume = [float(kline_info[k][5]) for k in range(0, len(kline_info))]
        close_time = [kline_info[k][6] for k in range(0, len(kline_info))]
        quote_vol = [float(kline_info[k][7]) for k in range(0, len(kline_info))]
        num_trades = [kline_info[k][8] for k in range(0, len(kline_info))]
        taker_buy_base_asset_volume = [kline_info[k][9] for k in range(0, len(kline_info))]
        taker_buy_quote_asset_volume = [kline_info[k][10] for k in range(0, len(kline_info))]

        kline_info = pd.DataFrame(columns = ['open_time', 'close_time', 'Open', 'High', 'Low', 'Close',
                                             'volume', 'quote_asset_volume', 'num_trades',
                                             'taker_buy_base_asset_volume'])
        kline_info['open_time'] = open_time
        kline_info['close_time'] = close_time
        kline_info['Open'] = open_price
        kline_info['High'] = high_price
        kline_info['Low'] = low_price
        kline_info['Close'] = close_price
        kline_info['volume'] = volume
        kline_info['quote_asset_volume'] = quote_vol
        kline_info['num_trades'] = num_trades
        kline_info['taker_buy_base_asset_volume'] = taker_buy_base_asset_volume
        kline_info['taker_buy_quote_asset_volume'] = taker_buy_quote_asset_volume

        return kline_info

    # bid 1 and ask 1 info：
    def bookTicker(self, symbol):

        r = self.s.get('%s/api/v3/ticker/bookTicker?symbol=%s' % (self.host, symbol))
        bookTicker = json.loads(r.content)

        return bookTicker