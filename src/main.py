from Logger import Logger
from TestTrader import TestTrader
from BacktestMarket import BacktestMarket
from BinanceMarket import BinanceMarket
from Asset import Asset
from Portfolio import Portfolio
import datetime
import time
import Metric
from LinearRegressionTrader import LinearRegressionTrader

def main():
  exampleBacktesting()

def exampleFronttesting():
  logger = Logger()
  logger.addTarget('log/fronttestlog.txt')

  portfolio = Portfolio(1000)
  portfolio.addAsset(Asset('ethereum', 'ETH'))

  end_date  = datetime.datetime(2019, 2, 15)
  timeframe = datetime.timedelta(minutes=5)

  apiKey  = 'SOME BINANCE API KEY'
  privKey = 'SOME BINANCE PRIV KEY'

  trader = TestTrader(portfolio, logger, 0)
  trader.fronttest(apiKey, privKey, end_date, timeframe)

def exampleBacktesting():
  logger = Logger()
  logger.addTarget('log/backtestlog.txt')

  start    = datetime.datetime(2019, 2, 10)
  end      = datetime.datetime(2019, 2, 25)
  interval = datetime.timedelta(days=5)

  portfolio = Portfolio(1000)
  portfolio.addAsset(Asset('ethereum', 'ETH'))
  asset = Asset('ethereum', 'ETH')

  metrics_list = [
    "burn_rate"              ,
    "transaction_volume"     ,
    "exchange_funds_flow"    ,
    "price"
  ]
  start_train    = datetime.datetime(2018, 12, 1)
  end_train      = datetime.datetime(2019, 1, 30)

  trader = LinearRegressionTrader(portfolio, logger, 0, metrics_list, asset)
  trader.train(start_train, end_train, interval)

  trader.backtest(start, end, interval)

def exampleBinance():
  logger = Logger()
  logger.addTarget('log/log.txt', 0)

  portfolio = Portfolio()
  portfolio.addAsset(Asset('ethereum', 'ETH'))

  apiKey  = 'insert api key here'
  privKey = 'insert private key here'
  market  = BinanceMarket(apiKey, privKey)

  end = datetime.datetime(2019, 1, 25)
  tf  = datetime.timedelta(minutes=5)

  trader = TestTrader(portfolio, logger, 0)
  trader.trade(market, end, tf)

if __name__ == '__main__':
    main()
