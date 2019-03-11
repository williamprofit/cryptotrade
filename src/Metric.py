import san
import sys
from Asset import Asset
import datetime
import time
import numpy as np

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
  if type(time) == type(datetime.datetime):
    time = reformatTime(time)

  if isMetricCached(metric, asset, time):
    return getCachedMetric(metric, asset, time)

  data = METRIC_FUNC_DIC[metric][0](metric, asset, time, args)
  cacheMetric(metric, asset, time, data)

  return data

# Loads a metric into cache
def loadMetric(metric, asset, start, end, interval, args=[]):
  _start = start
  _end   = start

  while True:
    _end = min(getEndForComplexity(_start, interval, MAX_COMPLEXITY), end)

    METRIC_FUNC_DIC[metric][1](metric, asset, _start, _end, interval, args)

    if _end == end:
      return

    _start = _end
    _end   = end

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
  for i in range(len(data.index)):
    time = santimentTimeToDatetime(data.index[i])
    cacheMetric(metric, asset, time, data.values[i])

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
  fillMissingData(start, end, interval, data)
  cacheSantimentMetric(metric, asset, start, interval, data[UNIT])

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
def getSocialMessages(metric, asset, time, args):
  assert len(args) > 1

  start    = getSanStartTime(time)
  end      = getSanEndTime(time)
  interval = getSanInterval()

  data = san.get(
    ('topic_search/messages')
  , source      = SOCIAL_SOURCE_TYPES[args[0]]
  , search_text = args[1]
  , from_date   = start.isoformat()
  , to_date     = end.isoformat()
  , interval    = intervalISOFormat(interval)
  )

  return data['messages'].values

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

  #TODO: rm
  if not isMetricCached(metric, asset, time):
    print('!!! MISSING DATA !!!', metric, asset, time)

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
                  , 'social_messages'        : (getSocialMessages, None)
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

def santimentTimeToDatetime(san_time):
  # Remove the milliseconds/microseconds
  san_time = str(san_time).partition('+')[0]

  return datetime.datetime.strptime(san_time, "%Y-%m-%d %H:%M:%S")

# Converts a datetime.timedelta() object to ISO format for Santiment
def intervalISOFormat(interval):
  shortcode = ""
  seconds = int(interval.total_seconds())

  s_in_d = 60 * 60 * 24
  s_in_h = 60 * 60
  if (seconds % s_in_d == 0):
    shortcode = str(seconds // s_in_d) + 'd'
  elif (seconds % s_in_h == 0):
    shortcode = str(seconds // s_in_h) + 'h'
  else:
    shortcode = str(seconds // 60) + 'm'

  return shortcode

# How much data we should fetch around a given time
sanTimeDelta = datetime.timedelta(days=1)

MAX_COMPLEXITY = 2000

def getDataComplexity(start, end, interval):
  return int((end - start) / interval)

def getEndForComplexity(start, interval, complexity):
  return start + interval * complexity

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
  new = time.replace(minute=myround(time.minute), second=0, microsecond=0)
  return new

def fillMissingData(start, end, interval, data):
  curr = start
  i    = 0
  while curr != end:
    san_date = santimentTimeToDatetime(data.index[i])
    if curr != san_date:
      if i == 0:
        avg = data.values[0]
      elif i == len(data) - 1:
        avg = data.values[len(data) - 1]
      else:
        prev_date = santimentTimeToDatetime(data.index[i-1])
        next_date = santimentTimeToDatetime(data.index[i+1])
        avg = (data.values[i-1] + data.values[i-2]) / ((next_date - prev_date) / interval)

      index = curr.isoformat()
      index = index[:10] + ' ' + index[11:]
      data.loc[index] = avg

    curr += interval
    i    += 1

# --------------------- #
# --- Usage example --- #
# --------------------- #

if __name__ == '__main__':
  # Note: preceed any function call with Metric.