import san
import sys
from Asset import Asset
import datetime
import time

import ccxt

# ---------------- Instructions ---------------- #
# To add a metric, create a function of the form #
# myMetric(metric, asset, time, args) and return #
# the specific data. Add my_metric : myMetric to #
# the METRIC_FUNC_DIC dictionary at the end of   #
# the file.                                      #
# ---------------------------------------------- #

san.ApiConfig.api_key = '2qirz5n6cygim57mxsaux35mu3g4ciuj_42omuqmk7fkmlwjw6d3na2lueuou73pt'

SOCIAL_VOLUME_TYPES = ["PROFESSIONAL_TRADERS_CHAT_OVERVIEW",
                      "TELEGRAM_CHATS_OVERVIEW",
                      "TELEGRAM_DISCUSSION_OVERVIEW",
                      "DISCORD_DISCUSSION_OVERVIEW"]

SOCIAL_SOURCE_TYPES = ["TELEGRAM",
                      "PROFESSIONAL_TRADERS_CHAT",
                      "REDDIT",
                      "DISCORD"]

metric_dic = {
  "daily_active_addresses" : "activeAddresses",
  "network_growth"         : "newAddresses",
  "burn_rate"              : "burnRate",
  "transaction_volume"     : "transactionVolume",
  "github_activity"        : "activity",
  "dev_activity"           : "activity",
  "exchange_funds_flow"    : "inOutDifference"
}

DATETIME_LENGTH = 19
UNIT = 'priceUsd'

METRIC_CACHE = {} # Is a 3D dict


# A Binance exchange is needed to query live data
exchange = ccxt.binance()

def setBinanceKeys(apiKey, secretKey):
  exchange.apiKey = apiKey
  exchange.secret = secretKey

# ------------------------ #
# --- Metric functions --- #
# ------------------------ #

# Returns the specified metric for any given asset at any given time
def getMetric(metric, asset, time, args=[]):
  time = reformatTime(time)

  if isMetricCached(metric, asset, time):
    return getCachedMetric(metric, asset, time)

  data = METRIC_FUNC_DIC[metric](metric, asset, time, args)
  cacheMetric(metric, asset, time, data)

  return data

# Returns whether a certain datapoint exists in cache
def isMetricCached(metric, asset, time):
  if not asset.symbol in METRIC_CACHE:
    return False
  if not metric in METRIC_CACHE[asset.symbol]:
    return False
  if not time in METRIC_CACHE[asset.symbol][metric]:
    return False

  return True

# Caches a single datapoint for any given metric, asset and time
def cacheMetric(metric, asset, time, data):
  if not asset.symbol in METRIC_CACHE:
    METRIC_CACHE[asset.symbol] = {}
  if not metric in METRIC_CACHE[asset.symbol]:
    METRIC_CACHE[asset.symbol][metric] = {}

  METRIC_CACHE[asset.symbol][metric][time] = data

# Caches big chunks of santiment data
def cacheSantimentMetric(metric, asset, start, interval, data):
  i = 0
  for d in data:
    cacheMetric('price', asset, start + i * interval, d)
    i += 1

# PRE: the metric IS stored in cache (see isMetricCached())
def getCachedMetric(metric, asset, time):
  return METRIC_CACHE[asset.symbol][metric][time]

# TODO: pre download metrics in cache to reduce latency
def loadMetric(metric, asset, start, end, interval):
  pass

# Queries Binance for live bid price of a certain asset (time arg is not used)
def getPriceBid(metric, asset, time, args):
  orderbook = exchange.fetch_order_book(asset.symbol + '/USDT')
  return orderbook['bids'][0][0]

# Queries Binance for live ask price of a certain asset (time arg is not used)
def getPriceAsk(metric, asset, time, args):
  orderbook = exchange.fetch_order_book(asset.symbol + '/USDT')
  return orderbook['asks'][0][0]

# Get historical price of an asset. Should be used strictly for historical data.
# For live data, use price_bid and price_ask (queries Binance)
def getPrice(metric, asset, time, args):
  start    = getSanStartTime(time)
  end      = getSanEndTime(time)
  interval = getSanInterval()

  data = san.get(
    ("prices/" + asset.slug)
  , from_date = start.isoformat()
  , to_date   = end.isoformat()
  , interval  = intervalISOFormat(interval)
  )

  # Cache all the data
  cacheSantimentMetric(metric, asset, start, interval, data[UNIT])

  index = timeToSantimentIndex(time, start, interval)
  return data[UNIT][index]

def getPriceOpen(metric, asset, time, args):
  pass

def getPriceClose(metric, asset, time, args):
  pass

def getPriceHi(metric, asset, time, args):
  pass

def getPriceLo(metric, asset, time, args):
  pass

def getVolume(metric, asset, time, args):
  pass

# PRE: args[0] contains the social volume type (as int)
def getSocialVolume(metric, asset, time, args):
  assert len(args) > 0

  start    = getSanStartTime(time)
  end      = getSanEndTime(time)
  interval = getSanInterval()

  data = san.get(
    ('social_volume/' + asset.slug)
  , from_date = start.isoformat()
  , to_date   = end.isoformat()
  , interval  = intervalISOFormat(interval)
  , social_volume_type = SOCIAL_VOLUME_TYPES[args[0]]
  )

  cacheSantimentMetric(metric , asset, start, interval, data['mentionsCount'])

  index = timeToSantimentIndex(time, start, interval)
  return data['mentionsCount'][index]

# PRE: args[0] contains the social sources type (as int)
# and  args[1] contains the search text
def getSocialChartData(metric, asset, time, args):
  assert len(args) > 1

  start    = getSanStartTime(time)
  end      = getSanEndTime(time)
  interval = getSanInterval()

  data = san.get(
    ('topic_search/chart_data')
  , source      = SOCIAL_SOURCE_TYPES[args[0]]
  , search_text = args[1]
  , from_date   = start.isoformat()
  , to_date     = end.isoformat()
  , interval    = intervalISOFormat(interval)
  )

  cacheSantimentMetric(metric, asset, start, interval, data['chartData'])
  index = timeToSantimentIndex(time, start, interval)

  return data['chartData'][index]['mentionsCount']

# PRE: args[0] contains the social source type (as int)
# and  args[1] contains the search text
def getSocialMessages(metric, asset, time, args):
  assert len(args) > 1

  start    = getSanStartTime(time)
  end      = getSanEndTime(time)
  interval = getSanInterval()

  data = san.get(
    ("topic_search/messages")
  , source      = SOCIAL_SOURCE_TYPES[args[0]]
  , search_text = args[1]
  , from_date   = start.isoformat()
  , to_date     = end.isoformat()
  , interval    = intervalISOFormat(interval)
  )

  cacheSantimentMetric(metric, asset, start, interval, data['messages'])

  return data['messages'].values

# Generic function to get a santiment metric (should not be used as-is, use getMetric(..))
def getSantimentMetric(metric, asset, time, args):
  start    = getSanStartTime(time)
  end      = getSanEndTime(time)
  interval = getSanInterval()

  data = san.get(
    (metric_dic[metric] + "/" + asset.slug)
  , from_date = start.isoformat()
  , to_date   = end.isoformat()
  , interval  = intervalISOFormat(interval)
  )

  cacheSantimentMetric(metric, asset, start, interval, data[metric_dic[metric]])

  index = timeToSantimentIndex(time, start, interval)
  return data[metric_dic[metric]][index]


# Dictionary that pairs a metric with its function
METRIC_FUNC_DIC = { 'price_bid'              : getPriceBid
                  , 'price_ask'              : getPriceAsk
                  , 'price'                  : getPrice
                  , 'daily_active_addresses' : getSantimentMetric
                  , 'network_growth'         : getSantimentMetric
                  , 'burn_rate'              : getSantimentMetric
                  , 'transaction_volume'     : getSantimentMetric
                  , 'github_activity'        : getSantimentMetric
                  , 'dev_activity'           : getSantimentMetric
                  , 'exchange_funds_flow'    : getSantimentMetric
                  , 'social_volume'          : getSocialVolume
                  , 'social_chart_data'      : getSocialChartData
                  , 'social_messages'        : getSocialMessages
                  }

# ------------------------ #
# --- Helper functions --- #
# ------------------------ #

# Converts a given time to an index to index arrays of data from Santiment
def timeToSantimentIndex(time, start, interval):
  difference = time - start
  remainder  = difference % interval

  if remainder >= interval / 2:
    difference += interval - remainder
  else:
    difference -= remainder

    index = difference // interval

  return index

# Converts a datetime.timedelta() object to ISO format for Santiment
def intervalISOFormat(interval):
  shortcode = ""
  seconds = int(interval.total_seconds())

  s_in_d = 60 * 60 * 24
  s_in_h = 60 * 60
  if (seconds % s_in_d == 0):
    shortcode = str(seconds // s_in_d) + "d"
  elif (seconds % s_in_h == 0):
    shortcode = str(seconds // s_in_h) + "h"
  else:
    shortcode = str(seconds // 60) + "m"

  return shortcode

# Returns the start time at which we should query Santiment for data
def getSanStartTime(time):
  return time.replace(hour=0, minute=0) - datetime.timedelta(days=1)

# Returns the end time at which we should query Santiment for data
def getSanEndTime(time):
  return time.replace(hour=0, minute=0) + datetime.timedelta(days=1)

# Returns the interval at which Santiment should send us data
def getSanInterval():
  return datetime.timedelta(minutes=5)

def myround(x, base=5):
    return int(base * round(float(x)/base))

# Keep only minutes and round them to nearest 5
def reformatTime(time):
  new = time.replace(minute=myround(time.minute) ,second=0, microsecond=0)
  return new


# --------------------- #
# --- Usage example --- #
# --------------------- #

if __name__ == '__main__':
  # Note: preceed any function call with Metric.

  setBinanceKeys('0xWlkQiiwKnhFYleIAKhJpKVfloVbnoianTsWgz9DOM7OEoB5ui2rEXEy4CHDI8C'
                ,'ldVscclShb30odBaL6lh6ZGB9tHwLPeSlWjgeDTKZOtCso2OU25TyWkbOnP0GyOt')

  ass = Asset('ethereum', 'ETH')

  print(getMetric('price', ass, datetime.datetime(2018, 3, 1, 12, 0)))
  print(getMetric('price_bid', ass, datetime.datetime.now()))
  print(getMetric('social_volume', ass, datetime.datetime(2019, 1, 12, 0, 0), [3, 'buy']))