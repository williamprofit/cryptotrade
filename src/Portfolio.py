from Asset import Asset

class Portfolio:
  def __init__(self, amountUSDT=0):
    self.assets = []
    self.assets.append(Asset('tether', 'USDT', amountUSDT))

  def addAsset(self, asset):
    self.assets.append(asset)

  def getAsset(self, symbol):
    for asset in self.assets:
      if asset.symbol == symbol:
        return asset

  def updateAsset(self, symbol, amount):
    self.getAsset(symbol).amount = amount

  def print(self):
    print(self.__str__())

  def __str__(self):
    string = 'Portfolio:\n'
    for asset in self.assets:
      string = string + ' - ' + asset.symbol + ': ' + str(asset.amount)

      if asset.init_amount != 0:
        string = string + ' ROI: ' + str(asset.ROI() * 100) + '%'

      string = string + '\n'

    return string[:-1]
