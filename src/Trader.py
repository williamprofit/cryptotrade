from datetime import datetime
from BacktestMarket import BacktestMarket
from FronttestMarket import FronttestMarket
import time

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

    last_action     = datetime(2000, 1, 1)
    self.curr_time  = datetime.now()

    while datetime.now() <= end_date:
      if datetime.now() - last_action >= self.timeframe:
        last_action    = datetime.now()
        self.curr_time = datetime.now()

        self.action()
        self.postAction()

        time.sleep(timeframe.total_seconds() - 1)

    self.finalAction()

  def backtest(self, start_date, end_date, timeframe):
    self.timeframe = timeframe
    self.market    = BacktestMarket(start_date, end_date, self.timeframe)
    self.market.setTransactionFees(0.0001)
    self.market.setLogger(self.logger, self.log_level)
    self.market.setPortfolio(self.portfolio)

    self.curr_time = start_date

    while self.curr_time < end_date:
      self.market.setDate(self.curr_time)

      self.action()
      self.postAction()

      self.curr_time = self.curr_time + self.timeframe

    self.finalAction()

  def fronttest(self, apiKey, privKey, end_date, timeframe):
    self.timeframe = timeframe
    self.market    = FronttestMarket(self.timeframe, apiKey, privKey)
    self.market.setTransactionFees(0.0001)
    self.market.setLogger(self.logger, self.log_level)
    self.market.setPortfolio(self.portfolio)

    last_action     = datetime(2000, 1, 1)
    self.curr_time  = datetime.now()

    while datetime.now() <= end_date:
      if datetime.now() - last_action >= self.timeframe:
        last_action    = datetime.now()
        self.curr_time = datetime.now()

        self.action()
        self.postAction()

        time.sleep(timeframe.total_seconds() - 1)

    self.finalAction()

  def action(self):
    pass

  def postAction(self):
    pass

  def finalAction(self):
    self.logger.log('Done.', self.log_level)
    self.logger.log(str(self.portfolio), self.log_level)