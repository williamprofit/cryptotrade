import sys
from Logger import Logger

class Market:
  def __init__(self):
    self.logger    = Logger()
    self.log_level = 0

  def buy(self, asset, amount):
    self.checkAmount(amount)
    msg = ('BUY  order. Symbol: ' + str(asset.symbol)
                + ' Percentage: ' + str(amount)
                    + ' Amount: ' + str(asset.amount * amount))

    self.logger.log(msg , self.log_level)

  def sell(self, asset, amount):
    self.checkAmount(amount)
    msg = ('SELL order. Symbol: ' + str(asset.symbol)
                + ' Percentage: ' + str(amount)
                    + ' Amount: ' + str(asset.amount * amount))

    self.logger.log(msg , self.log_level)

  def checkAmount(self, amount):
    if (amount < 0 or amount > 1):
      print('ERROR: amount to be traded must be between 0 and 1 (as a percentage)')
      print('STOPPING.')
      sys.exit(-1)

  def setPortfolio(self, portfolio):
    self.portfolio = portfolio

  def setLogger(self, logger, log_level):
    self.logger    = logger
    self.log_level = log_level