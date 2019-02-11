import Metric
import datetime
from Asset import Asset

def currentMetricsArrayGenerator(asset, start_time, end_time, timeframe, metrics_list):
    metrics_array = []
    time_at_moment = start_time

    while time_at_moment < end_time - timeframe:

        metrics_in_moment = []
        for metric in metrics_list:
            metrics_in_moment.append(Metric.getMetric(metric, asset, time_at_moment))
        metrics_array.append(metrics_in_moment)
        time_at_moment += timeframe

    return metrics_array


def futurePricesListGenerator(asset, start_time, end_time, timeframe):
    price_list = []
    time_at_future = start_time + timeframe

    while time_at_future < end_time:
        price_list.append(Metric.getMetric("price", asset, time_at_future))
        time_at_future += timeframe

    return price_list

def normalize(column):
    max_column = max(column)
    column = [x/max_column for x in column]

    return column


def train(start_training, end_training, timeframe, asset, metrics_list):
    for metric in metrics_list:
      Metric.loadMetric(metric, asset, start_training, end_training, timeframe) 

    current_metrics_array = currentMetricsArrayGenerator(asset, start_training, end_training, timeframe, metrics_list)
    future_prices_list    = futurePricesListGenerator(asset, start_training, end_training, timeframe)
    for n in range(len(current_metrics_array[0])):
        u = [x[n] for x in current_metrics_array]
        u = normalize(u)
        for row in range(len(current_metrics_array)):
            current_metrics_array[row][n] = u[row]
    
    return current_metrics_array, future_prices_list


