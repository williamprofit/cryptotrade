from Trader import Trader
import random

class TestTrader(Trader):
  def __init__(self, portfolio, logger, log_level):
    super().__init__(portfolio, logger, log_level)
    self.last_action = 'buy'

  def action(self):
    super().action()

    asset = self.portfolio.getAsset('ETH')

    if self.last_action == 'buy':
      self.market.sell(asset, 1)
      self.last_action = 'sell'
    else:
      self.market.buy(asset, 1)
      self.last_action = 'buy'

  def finalAction(self):
    asset = self.portfolio.getAsset('ETH')
    self.market.sell(asset, 1)

    super().finalAction()