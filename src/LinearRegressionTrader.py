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
from Portfolio import Portfolio



class LinearRegressionTrader(Trader):

  def __init__(self, portfolio, logger, log_level, metrics_list, asset):
    super().__init__(portfolio, logger, log_level)
    self.metrics_list = metrics_list
    self.ass = asset


  def train(self, start_training, end_training, timeframe):
    for metric in self.metrics_list:
      Metric.loadMetric(metric, self.ass, start_training, end_training, timeframe) 
    
    for social_platform_number in range (0,4):
      Metric.loadMetric("social_chart_data", self.ass, start_training, end_training, timeframe, args =[social_platform_number, "ethereum"]) 
    
    current_metrics_array = self.currentMetricsArrayGenerator(self.ass, start_training, end_training, timeframe)
    future_prices_list = self.futurePricesListGenerator(self.ass, start_training, end_training, timeframe)
    self.linear_model = self.regression(current_metrics_array, future_prices_list)


  def currentMetricsArrayGenerator(self, asset, start_time, end_time, timeframe):
    metrics_array = []
    time_at_moment = start_time

    while time_at_moment < end_time - timeframe:
      metrics_in_moment = []
      for metric in self.metrics_list:
        metrics_in_moment.append(Metric.getMetric(metric, asset, time_at_moment))
      for social_platform_number in range (0,4):
         metrics_in_moment.append(Metric.getMetric(metric, asset, time_at_moment, args =[social_platform_number, "ethereum"])) 
      
      metrics_array.append(metrics_in_moment)
      time_at_moment += timeframe

    return metrics_array


  def futurePricesListGenerator(self, asset, start_time, end_time, timeframe):
    price_list = []
    time_at_future = start_time + timeframe

    while time_at_future < end_time:
      price_list.append(Metric.getMetric("price", asset, time_at_future))
      time_at_future += timeframe

    return price_list


  def regression(self, past_data, future_data):
    X = past_data
    y = future_data
    lm = sklearn.linear_model.LinearRegression()
    lm.fit(X,y)
    print(y)
    print(lm.predict(X))


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
    
    for social_platform_number in range (0,4):
      list_of_metric_values.append(Metric.getMetric("social_chart_data", self.ass, now, args =[social_platform_number, "ethereum"])) 

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
