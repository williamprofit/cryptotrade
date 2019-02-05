from Logger import Logger

from TestTrader import TestTrader
from BacktestMarket import BacktestMarket
from BinanceMarket import BinanceMarket
from Asset import Asset
from Portfolio import Portfolio
import datetime
import time
import Metric

def main():
  exampleBacktesting()

def exampleFronttesting():
  logger = Logger()
  logger.addTarget('log/fronttestlog.txt')

  portfolio = Portfolio(1000)
  portfolio.addAsset(Asset('ethereum', 'ETH'))

  end_date  = datetime.datetime(2019, 2, 15)
  timeframe = datetime.timedelta(minutes=5)

  apiKey  = '0xWlkQiiwKnhFYleIAKhJpKVfloVbnoianTsWgz9DOM7OEoB5ui2rEXEy4CHDI8C'
  privKey = 'ldVscclShb30odBaL6lh6ZGB9tHwLPeSlWjgeDTKZOtCso2OU25TyWkbOnP0GyOt'

  trader = TestTrader(portfolio, logger, 0)
  trader.fronttest(apiKey, privKey, end_date, timeframe)

def exampleBacktesting():
  logger = Logger()
  logger.addTarget('log/backtestlog.txt')

  start    = datetime.datetime(2018, 12, 1)
  end      = datetime.datetime(2019, 1, 1)
  interval = datetime.timedelta(days=1)

  portfolio = Portfolio(1000)
  portfolio.addAsset(Asset('ethereum', 'ETH'))

  trader = TestTrader(portfolio, logger, 0)
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
