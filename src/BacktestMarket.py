from Market import Market
import datetime
import Metric

class BacktestMarket(Market):
  def __init__(self, from_date, to_date, timeframe):
    super().__init__()

    self.from_date = from_date
    self.to_date   = to_date
    self.timeframe = timeframe

    self.curr_date = from_date
    self.fees = 0

  def buy(self, asset, amount):
    super().buy(asset, amount)

    balanceUSDT = self.portfolio.getAsset('USDT').amount
    price       = self.getPriceOfAsset(asset, self.curr_date)
    tax         = balanceUSDT * amount * self.fees

    self.logger.log(str(price))

    new_amount_asset = asset.amount + ((balanceUSDT - tax) * amount) / price
    new_balanceUSDT  = balanceUSDT - ((balanceUSDT - tax) * amount)

    self.portfolio.updateAsset(asset.symbol, new_amount_asset)
    self.portfolio.updateAsset('USDT', new_balanceUSDT)

  def sell(self, asset, amount):
    super().sell(asset, amount)

    balanceUSDT = self.portfolio.getAsset('USDT').amount
    price       = self.getPriceOfAsset(asset, self.curr_date)
    tax         = asset.amount * amount * price * self.fees

    self.logger.log(str(price))

    new_amount_asset = asset.amount - (asset.amount * amount)
    new_balanceUSDT  = balanceUSDT + asset.amount * amount * price - tax

    self.portfolio.updateAsset(asset.symbol, new_amount_asset)
    self.portfolio.updateAsset('USDT', new_balanceUSDT)

  def getPriceOfAsset(self, asset, date):
    return Metric.getMetric('price', asset, date)

  def setTransactionFees(self, fees):
    self.fees = fees

  def setDate(self, date):
    self.curr_date = date

  def setPortfolio(self, portfolio):
    super().setPortfolio(portfolio)

    for asset in self.portfolio.assets:
      # skip USDT
      if asset.symbol != 'USDT':
        Metric.loadMetric('price', asset, self.from_date,
          self.to_date, self.timeframe)