from datetime import datetime
from BacktestMarket import BacktestMarket

class Trader:
  def __init__(self, portfolio, timeframe):
    self.portfolio = portfolio
    self.timeframe = timeframe
    self.market    = None

  def trade(self, market, end_date):
    self.market = market
    last_action = datetime.now()

    while datetime.now() <= end_date:
      if datetime.now() - last_action >= self.timeframe:
        last_action = datetime.now()
        self.action()

  def backtest(self, start_date, end_date):
    self.market = BacktestMarket(start_date, end_date, self.timeframe)
    curr_date = start_date

    while curr_date <= end_date:
      curr_date = curr_date + self.timeframe
      self.market.setDate(curr_date)

      self.action()

  def action(self):
    pass