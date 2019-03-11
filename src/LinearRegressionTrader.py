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
import matplotlib.pyplot as plt

#This file uses a linear regression to predict the future price of a cryptocurrency based on other metrics. 

class LinearRegressionTrader(Trader):

  def __init__(self, portfolio, logger, log_level, metrics_list, asset):
    super().__init__(portfolio, logger, log_level)
    self.metrics_list = metrics_list
    self.ass = asset


  def train(self, start_training, end_training, timeframe):
    #Load list of values for all metrics
    for metric in self.metrics_list:
      Metric.loadMetric(metric, self.ass, start_training, end_training, timeframe) 
        
    #Initialize the array(inputs) and list(outputs) to be used to train the linear regression
    current_metrics_array = self.currentMetricsArrayGenerator(self.ass, start_training, end_training, timeframe)
    future_prices_list    = self.futurePricesListGenerator(self.ass, start_training, end_training, timeframe)

    #Train the linear model and set it as a global variable - to be used for future predictions
    self.linear_model     = self.regression(current_metrics_array, future_prices_list)


  def currentMetricsArrayGenerator(self, asset, start_time, end_time, timeframe):
    metrics_array = []
    time_at_moment = start_time

    #Loop for all times in the range of start_time to end_time
    while time_at_moment < end_time - timeframe:

      #Create a list of the values of all the required metrics at a particular moment
      metrics_in_moment = []
      for metric in self.metrics_list:
        metrics_in_moment.append(Metric.getMetric(metric, asset, time_at_moment))

      metrics_array.append(metrics_in_moment)
      time_at_moment += timeframe

    return metrics_array


  def futurePricesListGenerator(self, asset, start_time, end_time, timeframe):
    #Since the price list is supposed to be the outputs change initial time to be the one which can be predicted
    price_list = []
    time_at_future = start_time + timeframe

    #loop to find price at all separate points in time
    while time_at_future < end_time:
      price_list.append(Metric.getMetric("price", asset, time_at_future))
      time_at_future += timeframe

    return price_list


  def regression(self, past_data, future_data):
    X  = past_data
    y  = future_data

    #Load linear model from SKlearn
    lm = sklearn.linear_model.LinearRegression()

    #Train model
    lm.fit(X,y)
    
    #Return model to be used to predict other values
    return lm


  def prediction_at_time(self, list_of_metric_values):
    #Get prediciton from global linear model
    prediction = self.linear_model.predict(list_of_metric_values)
    return prediction


  def action(self):
    super().action()
    #Set value for time and asset
    asset = self.portfolio.getAsset('ETH')
    now   = self.curr_time
    

    #Load metrics values for the particular moment for predicition 
    list_of_metric_values = []
    for metric in self.metrics_list:
      list_of_metric_values.append(Metric.getMetric(metric, self.ass, now))
    

    #The model expects a 2D Array of values to predict, hence put list in a list
    list_of_metric_values = [list_of_metric_values]
    #Get predicted price and current price
    curr_price = Metric.getMetric("price", self.ass, now)
    pred_price = self.prediction_at_time(list_of_metric_values)
    #Buy if predicted price is higher than current
    if pred_price > curr_price:
      self.market.buy(asset, 1)
      

    #Sell if predicted price is lower than current
    elif pred_price < curr_price:
      self.market.sell(asset, 1)


  def finalAction(self):
    asset = self.portfolio.getAsset('ETH')
    self.market.sell(asset, 1)

    super().finalAction()
