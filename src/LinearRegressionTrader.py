from Trader import Trader
from Metric import Metric, MetricParams
import datetime
import math as m
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np


class LinearRegressionTrader(Trader):

  def __init__(self, portfolio, logger, log_level, metrics_list):
    super().__init__(portfolio, logger, log_level)
    self.metrics = metrics_list
    self.metrics_array = []
    self.price = []


  def backtest(self, start_date, end_date, timeframe):
    self.start = start_date
    self.end = end_date
    self.interval = timeframe
    self.params = MetricParams(start_date, end_date+timeframe, timeframe)
    self.metric = Metric(self.params, self.portfolio.getAsset('ETH'), self.metrics)
    self.metrics_array = self.metric.metricsArray()
    self.price = self.metric.getMetric("prices")
    self.price = self.price[1:]
    super().backtest(start_date, end_date, timeframe)


  def regression(self):
    y = np.array(self.price)

    X = np.array(self.metrics_array)
    X = [x[:-1] for x in X]
    print("X =")
    print(X)
    print("...")
    print("y =")
    print(y)


    X = np.reshape

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)
    lm = sklearn.linear_model.LinearRegression()
    lm.fit(X_train,y_train)
    predictions = lm.predict(X)

    return predictions


  def PredictionsAt(self, time):

    predictions = self.regression()
    difference = time - self.start
    remainder = difference % self.interval

    if (remainder >= self.interval / 2):
      difference += (self.interval - remainder)
    else:
      difference -= remainder

    index = difference // self.interval

    return index


  def action(self):
    super().action()
    predictions = self.regression()
    asset = self.portfolio.getAsset('ETH')
    now = self.curr_time

    index = self.PredictionsAt(now)
    prev_price = self.price[index-1]
    pred_price = predictions[index]
    curr_price = self.price[index]



    if pred_price > prev_price:
      self.market.buy(asset, 1)
      print(prev_price)
      print(pred_price)
      print(curr_price)

    elif pred_price < prev_price:
      self.market.sell(asset, 1)
      print(prev_price)
      print(pred_price)
      print(curr_price)


  def finalAction(self):
    asset = self.portfolio.getAsset('ETH')
    self.market.sell(asset, 1)

    super().finalAction()
