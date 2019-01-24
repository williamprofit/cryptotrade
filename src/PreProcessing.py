from Metric import Metric, MetricParams
from Asset import Asset
import numpy as np
import datetime

DATETIME_LENGTH = 19

class PreProcessing:
  def __init__(self):
    pass

  def maxCalculator(self, asset, metric_list):
    met = Metric()
    start_date = datetime.datetime(2017, 1, 1)
    end_date   = datetime.datetime(2019, 1, 1)
    interval   = datetime.timedelta(minutes = 5)
    params     = MetricParams(start_date, end_date, interval)
    dict_metrics_maxes = {}
    for metric in metric_list:
      array = met.getMetric(metric, asset, params)
      dict_metrics_maxes[metric] = max(array)

    return dict_metrics_maxes


  def normalize(self, dict_metrics_maxes, metrics_array, metrics_list):
    for n in range(len(metrics_list)):
      metric = metrics_list[n]
      metric_column = metrics_array[n][:]
      metric_column = [x/dict_metrics_maxes[metric] for x in metric_column]
      metrics_array[n][:] = metric_column

    return metrics_array

  def areSameDates(self, a, b):
    return a.isoformat()[:DATETIME_LENGTH] == b.isoformat()[:DATETIME_LENGTH]

  def fillMissing(self, dates, data, params):
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
