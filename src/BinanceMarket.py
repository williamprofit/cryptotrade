from Market import Market
import ccxt

class BinanceMarket(Market):
  def __init__(self, apiKey, secretKey):
    self.exchange = ccxt.binance()

    self.exchange.apiKey = apiKey
    self.exchange.secret = secretKey

  def buy(self, asset, amount):
    super(asset, amount)

    # Assume trading with USDT
    order = self.exchange.create_order(
      symbol = asset.symbol + '/USDT',
      type   = 'market',
      side   = 'buy',
      amount = amount
    )
    asset.amount = self.getBalance(asset.symbol)

    self.logger.log('ANSWER FROM BINANCE: ' + str(order), self.log_level)

  def sell(self, asset, amount):
    super(asset, amount)

    # Assume trading with USDT
    order = self.exchange.create_order(
      symbol = asset.symbol + '/USDT',
      type   = 'market',
      side   = 'sell',
      amount = amount
    )
    asset.amount = self.getBalance(asset.symbol)

    self.logger.log('ANSWER FROM BINANCE: ' + str(order), self.log_level)

  def getBalance(self, symbol=''):
    balance = self.exchange.fetch_free_balance()

    if symbol == '':
      return balance
    else:
      return balance[symbol]