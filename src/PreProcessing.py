from Metric import Metric, MetricParams
from Asset import Asset
import numpy as np
import datetime


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
