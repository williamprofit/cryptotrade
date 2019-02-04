from Market import Market
import Metric
from datetime import datetime

class FronttestMarket(Market):
  def __init__(self, timeframe, apiKey, privKey):
    super().__init__()

    self.fees = 0
    self.curr_date = datetime.now()

    Metric.setBinanceKeys(apiKey, privKey)

  def buy(self, asset, amount):
    super().buy(asset, amount)

    balanceUSDT = self.portfolio.getAsset('USDT').amount
    price       = Metric.getMetric('price_bid', asset, datetime.now())
    tax         = balanceUSDT * amount * self.fees

    new_amount_asset = asset.amount + ((balanceUSDT - tax) * amount) / price
    new_balanceUSDT  = balanceUSDT - ((balanceUSDT - tax) * amount)

    self.portfolio.updateAsset(asset.symbol, new_amount_asset)
    self.portfolio.updateAsset('USDT', new_balanceUSDT)

  def sell(self, asset, amount):
    super().sell(asset, amount)

    balanceUSDT = self.portfolio.getAsset('USDT').amount
    price       = Metric.getMetric('price_ask', asset, datetime.now())
    tax         = balanceUSDT * amount * self.fees

    new_amount_asset = asset.amount - (asset.amount * amount)
    new_balanceUSDT  = balanceUSDT + asset.amount * amount * price - tax

    self.portfolio.updateAsset(asset.symbol, new_amount_asset)
    self.portfolio.updateAsset('USDT', new_balanceUSDT)

    self.logger.log(str(self.portfolio))

  def setTransactionFees(self, fees):
    self.fees = fees