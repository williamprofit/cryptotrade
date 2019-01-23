class Market:
  def __init__(self):
    self.logger    = None
    self.log_level = 0

  def buy(self, asset, amount):
    self.logger.log('BUY order. Symbol: ' + asset.symbol
                            + ' Amount: ' + amount, self.log_level)

  def sell(self, asset, amount):
    self.logger.log('SELL order. Symbol: ' + asset.symbol
                             + ' Amount: ' + amount, self.log_level)

  def setLogger(self, logger, log_level):
    self.logger    = logger
    self.log_level = log_level