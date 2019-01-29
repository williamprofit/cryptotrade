from BacktestMarket import BacktestMarket
from Metric import Metric, MetricParams
from datetime import datetime

class FronttestMarket(BacktestMarket):
  def __init__(self, timeframe):
    self.fees = 0
    self.curr_date = datetime.now()

    start = datetime.now() - 9 * timeframe
    end   = datetime.now() - 5 * timeframe
    self.params = MetricParams(start, end, timeframe)

  def getPriceOfAsset(self, asset, date):
    return self.metric.getMetric('prices').data[0]

  def sell(self, asset, amount):
    super().sell(asset, amount)
    self.logger.log(str(self.portfolio))