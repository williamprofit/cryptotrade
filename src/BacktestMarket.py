from Market import Market
from Metric import Metric, MetricParams

class BacktestMarket(Market):
  def __init__(self, from_date, to_date, interval):
    self.params = MetricParams(from_date, to_date, interval)
    self.metric = Metric()

    self.fees = 0

    self.curr_date = from_date

  def buy(self, asset, amount):
    super(asset, amount)

  def sell(self, asset, amount):
    super(asset, amount)

  def setTransactionFees(self, fees):
    self.fees = fees

  def setLogger(self, logger, log_level):
    self.logger    = logger
    self.log_level = log_level

  def setDate(self, date):
    self.curr_date = date