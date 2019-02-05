from Trader import Trader
import Metric
from Asset import Asset
import datetime
import math as m
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime, timedelta



class LinearRegressionTrader(Trader):

  def __init__(self, portfolio, logger, log_level, metrics_list):
    super().__init__(portfolio, logger, log_level)
    self.metrics_list = metrics_list
    start_time = datetime(2017, 6, 1)
    end_time = datetime(2018, 6, 1)
    self.ass = Asset('ethereum', 'ETH')
    self.timeframe = timedelta(days=1)

    for metric in metrics_list:
      Metric.loadMetric(metric, self.ass, start_time, end_time, self.timeframe) 
    

    current_metrics_array = self.currentMetricsArrayGenerator(self.ass, start_time, end_time)
    future_prices_list = self.futurePricesListGenerator(self.ass, start_time, end_time)
    self.linear_model = self.regression(current_metrics_array, future_prices_list)



  def currentMetricsArrayGenerator(self, asset, start_time, end_time):
    metrics_array = []
    time_at_moment = start_time

    while time_at_moment < end_time - self.timeframe:
      metrics_in_moment = []
      for metric in self.metrics_list:
        metrics_in_moment.append(Metric.getMetric(metric, self.ass, time_at_moment))
      metrics_array.append(metrics_in_moment)
      time_at_moment += self.timeframe

    return metrics_array


  def futurePricesListGenerator(self, asset, start_time, end_time):
    price_list = []
    time_at_future = start_time + self.timeframe

    while time_at_future < end_time:
      price_list.append(Metric.getMetric("price", self.ass, time_at_future))
      time_at_future += self.timeframe

    return price_list


  def regression(self, past_data, future_data):
    X = past_data
    y = future_data
    lm = sklearn.linear_model.LinearRegression()
    lm.fit(X,y)


    return lm


  def prediction_at_time(self, list_of_metric_values):
    prediction = self.linear_model.predict(list_of_metric_values)

    return prediction


  def action(self):
    super().action()
    asset = self.portfolio.getAsset('ETH')

    now = self.curr_time
    list_of_metric_values = []
    for metric in self.metrics_list:
      list_of_metric_values.append(Metric.getMetric(metric, self.ass, now))
    list_of_metric_values = [list_of_metric_values]
    
    print(list_of_metric_values)
    curr_price = Metric.getMetric("price", self.ass, now)
    pred_price = self.prediction_at_time(list_of_metric_values)


    if pred_price > curr_price:
      self.market.buy(asset, 1)
      print(pred_price)
      print(curr_price)

    elif pred_price < curr_price:
      self.market.sell(asset, 1)
      print(pred_price)
      print(curr_price)



  def finalAction(self):
    asset = self.portfolio.getAsset('ETH')
    self.market.sell(asset, 1)

    super().finalAction()
