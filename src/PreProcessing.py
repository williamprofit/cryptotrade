from Metric import Metric, MetricParams
from Asset import Asset
import numpy as np


asset_list = {
"ethereum":0,
"bitcoin":1
}

class Maxes:

    def maxCreator(self, asset, list_metrics, asset_array, asset_list):

        if asset not in asset_list:
            return asset_array[asset_list[asset]]
        else:
            metric_list = [
                "daily_active_addresses",
                "network_growth",
                "burn_rate": "burnRate",
                "transaction_volume",
                "github_activity",
                "dev_activity",
                "exchange_funds_flow"]

            met = Metric()
            eth = Asset(asset)
            params = MetricParams("2017-01-01", "2019-01-01", "5m")

            for n in range(len(metrc_list)):
                Array = met.MetricsArray(eth, params, list_metrics)
