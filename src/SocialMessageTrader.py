from Trader import Trader
from Metric import Metric, MetricParams
import datetime
import math as m
import matplotlib.pyplot as plt
from PreProcessing import PreProcessing


class SocialMessageTrader(Trader):



  def __init__(self, portfolio, logger, log_level):
    super().__init__(portfolio, logger, log_level)
    pass

  def backtest(self, start_date, end_date, timeframe):
    self.params = MetricParams(start_date - timeframe, end_date + timeframe, timeframe)
    self.metric = Metric(self.params, self.portfolio.getAsset('ETH'), ['github_activity'])
    self.pre = PreProcessing()
    self.list_sources = ["TELEGRAM",
                      "PROFESSIONAL_TRADERS_CHAT",
                      "REDDIT",
                      "DISCORD"]
    for source in self.list_sources:
      self.metric.downloadSocialChartData(source, "ethereum")



    super().backtest(start_date, end_date, timeframe)


  def getSocialData(self, asset, time):

    social_value = 0

    for source in self.list_sources:
      social_value += self.metric.getMetricAt("s:"+source+":ethereum", time)

    return average_calc




  def action(self):
    super().action()

    asset = self.portfolio.getAsset('ETH')
    now = self.curr_time
    prev_social = self.getSocialData(asset, now - self.timeframe)
    curr_social = self.getSocialData(asset, now)
    self.chart_social = []


    if prev_social > curr_social:
      self.market.buy(asset, 1)
      print(curr_social)
      chart_social.append(curr_social)


    elif prev_social < curr_social:
      self.market.sell(asset, 1)
      print(curr_social)
      chart_social.append(curr_social)



  def finalAction(self):
    asset = self.portfolio.getAsset('ETH')
    self.market.sell(asset, 1)

    plt.plot(self.chart_social)
    plt.ylabel('price')
    plt.show()
    print(self.chart_social)

    super().finalAction()
