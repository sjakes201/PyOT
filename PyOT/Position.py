from PyOT.profitnloss import *
from PyOT.Data.Market_Quotes import stock_price_live
import PyOT.Option as ops
import decimal

#TODO: merge Position.py and profitnloss.py. The profitnloss functions can go here, make it less complicated?

class Positions:

    def __init__(self, name=""):
        self.name = name
        self.legs = []
        self.values = {"initial value": 0, "current value": 0}
        self.stats = Strategy()
        self.ticker = ""

    def add_leg(self, option):
        if self.ticker == "":
            self.ticker = option.TICKER
        if option.TICKER == self.ticker:
            self.legs.append(option)
            self.stats.open(option)
            option.updater.subscribe(option, self.refresh_value)
            if option.type == "SHORT":
                self.values["initial value"] += option.initial_premium
            elif option.type == "LONG":
                self.values["initial value"] -=  option.initial_premium
        else:
            print("ERROR: adding option to position for different ticker")
        self.refresh_value()

    #removing legs is for "oops didnt mean to add this", or removing it from the position altogether, NOT for closing something for profit.
    def remove_leg(self, option):
        if option in self.legs:
            self.legs.remove(option)
            self.stats.remove_via_parent(option)
            if option.type == "SHORT":
                self.values["initial value"] -= option.initial_premium
            elif option.type == "LONG":
                self.values["initial value"] += option.initial_premium
        self.refresh_value()

    def __repr__(self):
        return "{} {} worth ${}".format(self.ticker, self.name, self.values["current value"])

    def refresh_value(self, option = None, Data = None):
        if not option is None:
            for leg in self.stats.longs + self.stats.shorts:
                if leg.parent_pointer is option:
                    leg.update_premium(Data)

        self.values["current value"] = self.stats.payoff_precise(stock_price_live(self.ticker))
        print(f"{self.ticker} position updated to new value: {self.values['current value']}")
