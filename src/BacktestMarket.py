from Market import Market
from Metric import Metric, MetricParams

class BacktestMarket(Market):
  def __init__(self, from_date, to_date, interval):
    super().__init__()

    self.params = MetricParams(from_date, to_date, interval)
    self.curr_date = from_date
    self.fees = 0

  def buy(self, asset, amount):
    super().buy(asset, amount)

    balanceUSDT = self.portfolio.getAsset('USDT').amount
    price       = self.getPriceOfAsset(asset, self.curr_date)
    fees        = balanceUSDT * amount * self.fees

    new_amount_asset = asset.amount + ((balanceUSDT - fees) * amount) / price
    new_balanceUSDT  = balanceUSDT - ((balanceUSDT - fees) * amount)

    self.portfolio.updateAsset(asset.symbol, new_amount_asset)
    self.portfolio.updateAsset('USDT', new_balanceUSDT)

  def sell(self, asset, amount):
    super().sell(asset, amount)

    balanceUSDT = self.portfolio.getAsset('USDT').amount
    price       = self.getPriceOfAsset(asset, self.curr_date)
    tax         = asset.amount * amount * price * self.fees

    new_amount_asset = asset.amount - (asset.amount * amount)
    new_balanceUSDT  = balanceUSDT + asset.amount * amount * price - tax

    self.portfolio.updateAsset(asset.symbol, new_amount_asset)
    self.portfolio.updateAsset('USDT', new_balanceUSDT)

  def getPriceOfAsset(self, asset, date):
    return self.metric.getMetricAt('prices', date)

  def setTransactionFees(self, fees):
    self.fees = fees

  def setDate(self, date):
    self.curr_date = date

  def setPortfolio(self, portfolio):
    super().setPortfolio(portfolio)

    # Gather the prices of all the assets
    for asset in self.portfolio.assets:
      # skip USDT
      if asset.symbol == 'USDT':
        continue

      self.metric = Metric(self.params, asset, ['prices'])
      break
