import os
import pandas as pd
from util import *
from scipy.stats import norm
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

class portfolio(object):

    def __init__(self, symbols = ['GOOG','AAPL','GLD','XOM'],dates=pd.date_range(dt.datetime(2008, 1, 1), dt.datetime(2010, 12, 31)), allocs=[0.1,0.2,0.3,0.4], sv=1000000):
        self.data=get_data(symbols,dates)
        self.symbols=symbols
        self.allocs=allocs
        self.start_value=sv
        self.value=self.portfolio_value(self.data, self.allocs, self.start_value)
        self.VaR=self.VaR()

    def author(self):
        return 'Yun Wan'

    def portfolio_value(self, data, allocs, sv):
        data=data.fillna(method='backfill')
        data=data.fillna(method='ffill')
        prices = data[self.symbols]  # only portfolio symbols

        # Get daily portfolio value
        # add code here to compute daily portfolio values
        prices_test=prices.div(prices.iloc[0])
        prices_test1=prices_test.multiply(allocs)
        prices_test2=prices_test1.multiply(sv)
        port_val=prices_test2.sum(axis=1)
        return port_val

    def VaR(self, confidence=0.99):
        daily_ret = self.value.pct_change()
        self.adr = daily_ret.mean()
        self.sddr = daily_ret.std()
        alpha=norm.ppf(1-confidence, self.adr, self.sddr)
        return self.value.iloc[-1]*(-alpha)

    def Monte_Carlo_Sim(self, mu, vol, T=252 ):
        Monte_Carlo = []
        for  i in range(1000):
            daily_returns=np.random.normal(mu, vol, T)+1
            price_list=[self.value.iloc[-1]]

            for rt in daily_returns:
                price_list.append(price_list[-1]*rt)

            plt.plot(price_list)

            Monte_Carlo.append(price_list[-1])
        plt.show()


