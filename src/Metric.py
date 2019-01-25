import san
from Asset import Asset
import datetime
import time

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
  "daily_active_addresses": "activeAddresses",
  "network_growth": "newAddresses",
  "burn_rate": "burnRate",
  "transaction_volume": "transactionVolume",
  "github_activity": "activity",
  "dev_activity": "activity",
  "exchange_funds_flow": "inOutDifference"
}

class Metric:
  def __init__(self, params, asset, metrics=[]):
    self.params = params
    self.asset = asset
    self.cache = {}
    self.metrics = metrics
    self.downloadMetrics(metrics)

  def getMetric(self, metric):
    cacheData = []
    if (metric == "prices"):
      data = san.get(
        ("prices/"+self.asset.slug),
        from_date=params.getFromDate(),
        to_date=params.getToDate(),
        interval=params.getInterval()
      )
      cacheData = data[params.unit]
    elif (metric == "social_volume"):
      # pre: Asset has to be in sentiment's social_volume_projects
      data = san.get(
        ("social_volume/" + self.asset.slug),
        from_date=self.params.getFromDate(),
        to_date=self.params.getToDate(),
        interval=self.params.getInterval(),
        social_volume_type=SOCIAL_VOLUME_TYPES[self.params.SVT]
      )
      cacheData = data["mentionsCount"]
    else:
      data = san.get(
        (metric+"/"+self.asset.slug),
        from_date=params.getFromDate(),
        to_date=params.getToDate(),
        interval=params.getInterval()
      )
      cacheData = data[metric_dic[metric]]
    self.cache[metric] = cacheData
    return cacheData

  def metricsArray(self, list_metrics):
    metricsArray = []
    for metric_str in list_metrics:
      metric = self.getMetric(metric_str)
      metricsArray.append(metric)

    return metricsArray

  # pre: Asset has to be in sentiment's social_volume_projects
  def getSocialChartData(self, idx_type, search_text):
    data = san.get(
      ("topic_search/chart_data"),
      source=SOCIAL_SOURCE_TYPES[idx_type],
      search_text=search_text,
      from_date=params.from_date,
      to_date=params.to_date,
      interval=params.interval
    )
    return data["chartData"]

  def getSocialMessages(self, idx_type, search_text):
    data = san.get(
      ("topic_search/messages"),
      source=SOCIAL_SOURCE_TYPES[idx_type],
      search_text=search_text,
      from_date=params.from_date,
      to_date=params.to_date,
      interval=params.interval
    )
    return data["messages"]

  def downloadMetrics(self, metrics):
    for metric in metrics:
      self.getMetric(metric)

  def getMetricAt(self, metric, time):

    if metric in self.cache:
      data = self.cache[metric]
    else:
      data = self.getMetric(metric)

    differnce = time - params.from_date
    differnce_minutes = int(differnce.total_seconds()) // 60
    interval_minutes = int(params.interval.total_seconds()) // 60

    remainder = differnce_minutes % interval_minutes
    if (remainder >= interval_minutes / 2):
      differnce_minutes += (interval_minutes - remainder)
    else:
      differnce_minutes -= remainder

    index = differnce_minutes // interval_minutes

    if (index > len(data) or index < 0):
      print ("Error: trying to access data that's out of bounds")

    return data[index]

    def setParams(self, params):
      self.params = params

class MetricParams:
  def __init__(self, from_date, to_date, interval, SVT=0, unit="priceUsd"):
    self.from_date = from_date
    self.to_date   = to_date
    self.interval  = interval
    self.SVT  = SVT
    self.unit = unit

  def getToDate(self):
    return to_date.isoformat()

  def getFromDate(self):
    return from_date.isoformat()

  def getInterval(self):
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

# Leaving this here for now just so you can see how to set things up
if __name__ == '__main__':
  from_date = datetime.datetime(2018,1,1,  0, 0)
  to_date = datetime.datetime(2018, 1, 2,  0, 5)
  interval = datetime.timedelta(minutes=(5))
  params = MetricParams(from_date, to_date, interval)
  ass = Asset("ethereum", "ETH", 0)
  met = Metric(params, ass, ["prices"])

  specific_time = to_date - 2*interval

  print( met.getMetricAt("exchange_funds_flow", specific_time))