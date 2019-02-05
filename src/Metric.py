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

  data = METRIC_FUNC_DIC[metric][0](metric, asset, time, args)
  cacheMetric(metric, asset, time, data)

  return data

# Loads a metric into cache
def loadMetric(metric, asset, start, end, interval, args=[]):
  METRIC_FUNC_DIC[metric][1](metric, asset, start, end, interval, args)

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
    cacheMetric(metric, asset, start + i * interval, d)
    i += 1

# PRE: the metric IS stored in cache (see isMetricCached())
def getCachedMetric(metric, asset, time):
  return METRIC_CACHE[asset.symbol][metric][time]


def loadPrice(metric, asset, start, end, interval, args):
  data = san.get(
    ('prices/' + asset.slug)
  , from_date = start.isoformat()
  , to_date   = end.isoformat()
  , interval  = intervalISOFormat(interval)
  )

  # Cache all the data
  cacheSantimentMetric('price', asset, start, interval, data[UNIT])

# PRE: args[0] contains the social volume type (as int)
def loadSocialVolume(metric, asset, start, end, interval, args):
  assert len(args) > 0

  data = san.get(
    ('social_volume/' + asset.slug)
  , from_date = start.isoformat()
  , to_date   = end.isoformat()
  , interval  = intervalISOFormat(interval)
  , social_volume_type = SOCIAL_VOLUME_TYPES[args[0]]
  )

  cacheSantimentMetric(metric , asset, start, interval, data['mentionsCount'])

# PRE: args[0] contains the social sources type (as int)
# and  args[1] contains the search text
def loadSocialChartData(metric, asset, start, end, interval, args):
  assert len(args) > 1

  data = san.get(
    ('topic_search/chart_data')
  , source      = SOCIAL_SOURCE_TYPES[args[0]]
  , search_text = args[1]
  , from_date   = start.isoformat()
  , to_date     = end.isoformat()
  , interval    = intervalISOFormat(interval)
  )

  cacheSantimentMetric(metric, asset, start, interval, data['chartData'])

# PRE: args[0] contains the social source type (as int)
# and  args[1] contains the search text
def loadSocialMessages(metric, asset, start, end, interval, args):
  assert len(args) > 1

  data = san.get(
    ('topic_search/messages')
  , source      = SOCIAL_SOURCE_TYPES[args[0]]
  , search_text = args[1]
  , from_date   = start.isoformat()
  , to_date     = end.isoformat()
  , interval    = intervalISOFormat(interval)
  )

  cacheSantimentMetric(metric, asset, start, interval, data['messages'].values)

def loadSantimentMetric(metric, asset, start, end, interval, args):
  data = san.get(
    (metric + '/' + asset.slug)
  , from_date = start.isoformat()
  , to_date   = end.isoformat()
  , interval  = intervalISOFormat(interval)
  )

  cacheSantimentMetric(metric, asset, start, interval, data[metric_dic[metric]])

# Generic function to get a santiment metric (should not be used as-is, use getMetric(..))
def getSantimentMetric(metric, asset, time, args):
  start    = getSanStartTime(time)
  end      = getSanEndTime(time)
  interval = getSanInterval()

  loadMetric(metric, asset, start, end, interval, args)
  return getCachedMetric(metric, asset, time)


# Queries Binance for live bid price of a certain asset (time arg is not used)
def getPriceBid(metric, asset, time, args):
  orderbook = exchange.fetch_order_book(asset.symbol + '/USDT')
  return orderbook['bids'][0][0]

# Queries Binance for live ask price of a certain asset (time arg is not used)
def getPriceAsk(metric, asset, time, args):
  orderbook = exchange.fetch_order_book(asset.symbol + '/USDT')
  return orderbook['asks'][0][0]

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


# Dictionary that pairs a metric with its get and load functions.
# Note that sometimes a the load function might not exist eg for live data
METRIC_FUNC_DIC = { 'price_bid'              : (getPriceBid, None)
                  , 'price_ask'              : (getPriceAsk, None)
                  , 'price'                  : (getSantimentMetric, loadPrice)
                  , 'daily_active_addresses' : (getSantimentMetric, loadSantimentMetric)
                  , 'network_growth'         : (getSantimentMetric, loadSantimentMetric)
                  , 'burn_rate'              : (getSantimentMetric, loadSantimentMetric)
                  , 'transaction_volume'     : (getSantimentMetric, loadSantimentMetric)
                  , 'github_activity'        : (getSantimentMetric, loadSantimentMetric)
                  , 'dev_activity'           : (getSantimentMetric, loadSantimentMetric)
                  , 'exchange_funds_flow'    : (getSantimentMetric, loadSantimentMetric)
                  , 'social_volume'          : (getSantimentMetric, loadSocialVolume)
                  , 'social_chart_data'      : (getSantimentMetric, loadSocialChartData)
                  , 'social_messages'        : (getSantimentMetric, loadSocialMessages)
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

# How much data we should fetch around a given time
sanTimeDelta = datetime.timedelta(days=1)

# Returns the start time at which we should query Santiment for data
def getSanStartTime(time):
  return time.replace(hour=0, minute=0) - sanTimeDelta

# Returns the end time at which we should query Santiment for data
def getSanEndTime(time):
  return min(time.replace(hour=0, minute=0) + sanTimeDelta
            ,datetime.datetime.now() - datetime.timedelta(days=1))

# Returns the interval at which Santiment should send us data
def getSanInterval():
  return datetime.timedelta(minutes=5)

def myround(x, base=5):
    return int(base * round(float(x)/base))

# Keep only minutes and round them to nearest 5
def reformatTime(time):
  new = time.replace(minute=myround(time.minute) ,second=0, microsecond=0)
  return new

def fillMissingData(self, dates, data, params):
  current_datetime = params.from_date

  fixed_data = []
  i = 0
  latest_datetime = current_datetime
  while i < len(dates):
    if (self.areSameDates(dates[i], current_datetime)):
      fixed_data.append(data[i])
      latest_datetime = current_datetime
      current_datetime += params.interval
      i += 1
    else:
      counter = 1
      from_value = fixed_data[-1]
      to_value = data[i]
      temp_datetime = latest_datetime + params.interval

      while not (self.areSameDates(dates[i], temp_datetime)):
        counter += 1
        temp_datetime += params.interval

      to_value = data[i]
      increment = (to_value - from_value) / counter
      for j in range(1,counter):
        fixed_data.append(from_value + j * increment)

      current_datetime = latest_datetime + counter * params.interval
      latest_datetime = current_datetime

  return fixed_data



# --------------------- #
# --- Usage example --- #
# --------------------- #

if __name__ == '__main__':
  # Note: preceed any function call with Metric.

  setBinanceKeys('0xWlkQiiwKnhFYleIAKhJpKVfloVbnoianTsWgz9DOM7OEoB5ui2rEXEy4CHDI8C'
                ,'ldVscclShb30odBaL6lh6ZGB9tHwLPeSlWjgeDTKZOtCso2OU25TyWkbOnP0GyOt')

  ass = Asset('ethereum', 'ETH')

  print(getMetric('price', ass, datetime.datetime(2018, 3, 1, 12, 0)))
  print(getMetric('burn_rate', ass, datetime.datetime(2018, 3, 1, 12, 0)))
  print(getMetric('price_bid', ass, datetime.datetime.now()))
  print(getMetric('social_volume', ass, datetime.datetime(2019, 1, 12, 0, 0), [3, 'buy']))