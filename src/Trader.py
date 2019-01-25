from datetime import datetime
from BacktestMarket import BacktestMarket

class Trader:
  def __init__(self, portfolio, logger, log_level):
    self.portfolio = portfolio
    self.market    = None

    self.logger    = logger
    self.log_level = log_level

  def trade(self, market, end_date, timeframe):
    self.timeframe = timeframe
    self.market    = market
    self.market.setLogger(self.logger, self.log_level)
    self.market.setPortfolio(self.portfolio)

    last_action = datetime(2000, 1, 1)

    while datetime.now() <= end_date:
      if datetime.now() - last_action >= self.timeframe:
        last_action = datetime.now()
        self.action()
        self.postAction()

    self.finalAction()

  def backtest(self, start_date, end_date, timeframe):
    self.timeframe = timeframe
    self.market    = BacktestMarket(start_date, end_date, self.timeframe)
    self.market.setTransactionFees(0.0001)
    self.market.setLogger(self.logger, self.log_level)
    self.market.setPortfolio(self.portfolio)

    curr_date = start_date

    while curr_date < end_date:
      curr_date = curr_date + self.timeframe
      self.market.setDate(curr_date)

      self.action()
      self.postAction()

    self.finalAction()

  def action(self):
    pass

  def postAction(self):
    pass

  def finalAction(self):
    self.logger.log('Done.', self.log_level)
    self.logger.log(str(self.portfolio), self.log_level)