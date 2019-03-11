from Trader import Trader
from Metric import Metric, MetricParams
import datetime

# Naive trader for testing purposes
class TrendTrader(Trader):

  def backtest(self, start_date, end_date, timeframe):
    self.params = MetricParams(start_date - timeframe, end_date + timeframe, timeframe)
    self.metric = Metric(self.params, self.portfolio.getAsset('ETH'), ["prices"])

    super().backtest(start_date, end_date, timeframe)

  def getPrice(self, time):
    return self.metric.getMetricAt("prices", time)

  def isDownTrend(self):
    return self.getPrice(self.curr_time) <= self.getPrice(self.curr_time - self.timeframe)

  def action(self):
    asset = self.portfolio.getAsset('ETH')
    if self.isDownTrend():
      self.market.sell(asset, 0.7)
    else:
      self.market.buy(asset, 1)

  def finalAction(self):
    asset = self.portfolio.getAsset('ETH')
    self.market.sell(asset, 1)

    super().finalAction()
    