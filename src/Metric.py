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


class Metric:

    def __init__(self):
        pass

    def getDailyActiveAddresses(self, asset, params, unit="priceBtc"):
        data = prices = san.get(
            ("daily_active_addresses/"+asset.slug),
            from_date=params.from_date,
            to_date=params.to_date,
            interval=params.interval
        )
        return data["activeAddresses"]

    def getNetworkGrowth(self, asset, params):
        data = san.get(
            ("network_growth/"+asset.slug),
            from_date=params.from_date,
            to_date=params.to_date
        )
        return data["newAddresses"]

    def getBurnRate(self, asset, params):
        data = burn_rate = san.get(
            ("burn_rate/"+asset.slug),
            from_date=params.from_date,
            to_date=params.to_date,
            interval=params.interval
        )
        return data["burnRate"]

    def getTransactionVolume(self, asset, params):
        data = burn_rate = san.get(
            ("transaction_volume/"+asset.slug),
            from_date=params.from_date,
            to_date=params.to_date,
            interval=params.interval
        )
        return data["transactionVolume"]

    def getGitHubActivity(self, asset, params):
        data = burn_rate = san.get(
            ("github_activity/"+asset.slug),
            from_date=params.from_date,
            to_date=params.to_date,
            interval=params.interval
        )
        return data["activity"]

    def getDevActivity(self, asset, params):
        data = burn_rate = san.get(
            ("dev_activity/"+asset.slug),
            from_date=params.from_date,
            to_date=params.to_date,
            interval=params.interval
        )
        return data["activity"]

    def getPrices(self, asset, params, unit="priceBtc"):
        data = prices = san.get(
            ("prices/"+asset.slug),
            from_date=params.from_date,
            to_date=params.to_date,
            interval=params.interval
        )
        return data[unit]

    def getExchangeFundsFlow(self, asset, params):
        data = san.get(
            ("exchange_funds_flow/"+asset.slug),
            from_date=params.from_date,
            to_date=params.to_date,
            interval=params.interval
        )
        return data["inOutDifference"]

# pre: Asset has to be in sentiment's social_volume_projects
# social_volume_type
    def getSocialVolume(self, asset, params, idx_type):
        data = san.get(
            ("social_volume/" + asset.slug),
            from_date=params.from_date,
            to_date=params.to_date,
            interval=params.interval,
            social_volume_type=SOCIAL_VOLUME_TYPES[idx_type]
        )
        return data["mentionsCount"]

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
    def __init__(self, from_date, to_date, interval):
        self.from_date = from_date
        self.to_date = to_date
        self.interval = interval
