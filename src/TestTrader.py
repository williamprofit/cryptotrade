from Trader import Trader
import random

class TestTrader(Trader):
  def __init__(self, portfolio, timeframe):
    super(portfolio, timeframe)
    random.seed(0)

  #WIP
  def action(self):
    asset = self.portfolio[0]
    if random.randint(1, 100) > 50:
      self.market.buy(asset, asset.amount)
    else:
      self.market.sell(asset, asset.amount)