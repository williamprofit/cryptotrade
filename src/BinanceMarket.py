from Market import Market
import ccxt

class BinanceMarket(Market):
  def __init__(self, apiKey, secretKey):
    super().__init__()

    self.exchange = ccxt.binance()

    self.exchange.apiKey = apiKey
    self.exchange.secret = secretKey

    self.balance = None

  # Amount must be expressed as a percentage
  # Assume trading with USDT
  def buy(self, asset, amount):
    super().buy(asset, amount)

    balanceUSD = self.getBalance('USDT')

    order = self.exchange.create_order(
      symbol = asset.symbol + '/USDT',
      type   = 'market',
      side   = 'buy',
      amount = amount * balanceUSD
    )

    # Update asset & USDT amount
    self.refreshBalance()
    self.portfolio.updateAsset(asset.symbol, self.getBalance(asset.symbol))
    self.portfolio.updateAsset('USDT', self.getBalance('USDT'))

    self.logger.log('ANSWER FROM BINANCE: ' + str(order), self.log_level)

  # Amount must be expressed as a percentage
  # Assume trading with USDT
  def sell(self, asset, amount):
    super().sell(asset, amount)

    order = self.exchange.create_order(
      symbol = asset.symbol + '/USDT',
      type   = 'market',
      side   = 'sell',
      amount = amount * asset.amount
    )

    # Update asset & USDT amount
    self.refreshBalance()
    self.portfolio.updateAsset(asset.symbol, self.getBalance(asset.symbol))
    self.portfolio.updateAsset('USDT', self.getBalance('USDT'))

    self.logger.log('ANSWER FROM BINANCE: ' + str(order), self.log_level)

  def getBalance(self, symbol=''):
    if symbol == '':
      return self.balance
    else:
      return self.balance[symbol]

  def refreshBalance(self):
    self.balance = self.exchange.fetch_free_balance()

  def setPortfolio(self, portfolio):
    super().setPortfolio(portfolio)

    self.refreshBalance()
    for asset in self.portfolio.assets:
      asset.amount      = self.getBalance(asset.symbol)
      asset.init_amount = asset.amount

    self.logger.log('Portfolio initialized with Binance as follows', self.log_level)
    self.logger.log(str(self.portfolio), self.log_level)