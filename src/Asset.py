class Asset:
  def __init__(self, slug, symbol, amount):
    self.amount = amount
    self.slug   = slug
    self.symbol = symbol

    self.init_amount = amount

  def ROI(self):
    return (self.amount - self.init_amount) / self.init_amount