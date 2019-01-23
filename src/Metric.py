import san

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
    def __init__(self):
        pass

    def getMetric(self, metric, asset, params):
        if(metric == "prices"):
            data = san.get(
                ("prices/"+asset.slug),
                from_date=params.from_date,
                to_date=params.to_date,
                interval=params.interval
            )
            return data[params.unit]
        elif (metric == "social_volume"):
            # pre: Asset has to be in sentiment's social_volume_projects
            data = san.get(
                ("social_volume/" + asset.slug),
                from_date=params.from_date,
                to_date=params.to_date,
                interval=params.interval,
                social_volume_type=SOCIAL_VOLUME_TYPES[params.SVT]
            )
            return data["mentionsCount"]
        else:
            data = san.get(
                (metric+"/"+asset.slug),
                from_date=params.from_date,
                to_date=params.to_date,
                interval=params.interval
            )
            return data[metric_dic[metric]]

    def MetricsArray(self, asset, params, list_metrics):
        metricsArray = Metric().getMetric(list_metrics[0], asset, params)
        for i in range(1, len(list_metrics)):
            metricColumn = Metric().getMetric(list_metrics[i], asset, params)
            metricsArray = np.column_stack((metricsArray, metricColumn))

        return metricsArray


# pre: Asset has to be in sentiment's social_volume_projects

    def getSocialChartData(self, params, idx_type, search_text):
        data = san.get(
            ("topic_search/chart_data"),
            source=SOCIAL_SOURCE_TYPES[idx_type],
            search_text=search_text,
            from_date=params.from_date,
            to_date=params.to_date,
            interval=params.interval)
        return data["chartData"]

    def getSocialMessages(self, params, idx_type, search_text):
        data = san.get(
            ("topic_search/messages"),
            source=SOCIAL_SOURCE_TYPES[idx_type],
            search_text=search_text,
            from_date=params.from_date,
            to_date=params.to_date,
            interval=params.interval)
        return data["messages"]


class MetricParams:
    def __init__(self, from_date, to_date, interval, SVT=0):
        self.from_date = from_date
        self.to_date = to_date
        self.interval = interval
        self.SVT = SVT
        self.unit = "volume"
