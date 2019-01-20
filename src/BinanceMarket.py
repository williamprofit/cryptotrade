from Market import Market
import ccxt

class BinanceMarket(Market):
    def __init__(self, apiKey, secretKey):
        self.exchange = ccxt.binance()

        self.exchange.apiKey = apiKey
        self.exchange.secret = secretKey

        self.sell_orders = []
        self.buy_orders  = []

    def setLogger(self, logger, logLevel):
        self.logger   = logger
        self.logLevel = logLevel

    def buy(self, symbol, amount):
        order = self.exchange.create_order(symbol=symbol, type='market', side='buy', amount=amount)

        self.buy_orders.append(order)
        self.logger.log('BUY order. Symbol: ' + symbol + ' Amount: ' + amount, self.logLevel)

    def sell(self, symbol, amount):
        order = self.exchange.create_order(symbol=symbol, type='market', side='sell', amount=amount)

        self.sell_orders.append(order)
        self.logger.log('SELL order. Symbol: ' + symbol + ' Amount: ' + amount, self.logLevel)

    def getBalance(self, currency=''):
        balance = self.exchange.fetch_free_balance()

        if currency == '':
            return balance
        else:
            return balance[currency]
