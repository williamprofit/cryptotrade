from Market import Market
import ccxt

class BinanceMarket(Market):
    def __init__(self, symbol):
        self.exchange = ccxt.binance()
        self.symbol   = symbol

        self.sell_orders = []
        self.buy_orders  = []

    def setKeys(self, apiKey, secretKey):
        self.exchange.apiKey = apiKey
        self.exchange.secret = secretKey

    def setLogger(self, logger, logLevel):
        self.logger   = logger
        self.logLevel = logLevel

    def buy(self, amount):
        order = self.exchange.create_order(symbol=self.symbol, type='market', side='buy', amount=amount)

        self.buy_orders.append(order)
        self.logger.log('BUY order. Symbol: ' + self.symbol + ' Amount: ' + amount, self.logLevel)

    def sell(self, amount):
        order = self.exchange.create_order(symbol=self.symbol, type='market', side='sell', amount=amount)

        self.sell_orders.append(order)
        self.logger.log('SELL order. Symbol: ' + self.symbol + ' Amount: ' + amount, self.logLevel)

    def getBalance(self):
        balance = self.exchange.fetch_free_balance()
        # Filter out balances with 0
        return {k: v for k, v in balance.items() if v > 0}