from Trader import Trader
from Metric import Metric, MetricParams
import datetime
import math as m
import matplotlib.pyplot as plt
from PreProcessing import PreProcessing


class MovingAverageTrader(Trader):
  def __init__(self, portfolio, logger, log_level):
    super().__init__(portfolio, logger, log_level)
    pass

  def backtest(self, start_date, end_date, timeframe):
    self.params = MetricParams(start_date - timeframe, end_date + timeframe, timeframe)
    self.metric = Metric(self.params, self.portfolio.getAsset('ETH'), ['github_activity'])
    self.pre = PreProcessing()

    super().backtest(start_date, end_date, timeframe)


  def getGithubActivity(self, asset, time):

    average_calc = 0
    one_minute = datetime.timedelta(minutes=1)
    minutes_in_interval = m.floor(self.timeframe/one_minute)

    for i in range(minutes_in_interval):
      average_calc += self.metric.getMetricAt("github_activity", time - one_minute*i)
    average_calc = average_calc/minutes_in_interval
    return average_calc

  def getPrice(self, asset, time):
    price_at_moment = self.metric.getMetricAt("price", time)
    return price_at_moment



  def action(self):
    super().action()

    asset = self.portfolio.getAsset('ETH')
    now = self.curr_time
    prev_price = self.getPrice(asset, now - self.timeframe)
    curr_price = self.getPrice(asset, now)
    chart_price = []


    if prev_price > curr_price:
      self.market.buy(asset, 1)
      print(curr_price)
      chart_price.append(curr_price)
      print(chart_price)

    elif prev_price < curr_price:
      self.market.sell(asset, 1)
      print(curr_price)
      chart_price.append(curr_price)
      print(chart_price)


  def finalAction(self):
    asset = self.portfolio.getAsset('ETH')
    self.market.sell(asset, 1)

    plt.plot(chart_price)
    plt.ylabel('price')
    plt.show()
    print(chart_price)

    super().finalAction()
