from PyOT.Data.profitnloss import *
from PyOT.Data.Market_Quotes import stock_price_live
import PyOT.Option as ops

#TODO: merge Position.py and profitnloss.py. The profitnloss functions can go here, make it less complicated?

class Positions:
    def __init__(self, name=""):
        self.name = name
        self.legs = []
        self.values = {"initial value": 0, "current value": 0}
        self.stats = None
        self.ticker = ""

    def add_leg(self, option):
        if self.ticker == "":
            self.ticker = option.TICKER
        if option.TICKER == self.ticker:
            self.legs.append(option)
        else:
            print("ERROR: adding option to position for different ticker")

    def initialize(self):
        pos = Strategy()
        for leg in self.legs:
            if leg.type == "LONG":
                if type(leg) == ops.Call:
                    pos.BTO(Call_Option(leg.strike, leg.initial_premium, leg))
                elif type(leg) == ops.Put:
                    pos.BTO(Put_Option(leg.strike, leg.initial_premium, leg))
            elif leg.type == "SHORT":
                if type(leg) == ops.Call:
                    pos.STO(Call_Option(leg.strike, leg.initial_premium, leg))
                elif type(leg) == ops.Put:
                    pos.STO(Put_Option(leg.strike, leg.initial_premium, leg))
        self.stats = pos
    
        self.values["current value"] = self.values["initial value"] = pos.payoff_precise(stock_price_live(self.ticker))
    
        for leg in self.legs:
            leg.updater.subscribe(self, self.refresh_value)

    def __repr__(self):
        return "{} {} worth ${}".format(self.ticker, self.name, self.values["current value"])

    def refresh_value(self, option, Data):
        # pos = Strategy()
        # for leg in self.legs:
        #     if leg.type == "LONG":
        #         if type(leg) == ops.Call:
        #             pos.BTO(Call_Option(leg.strike, leg.current_value))
        #         elif type(leg) == ops.Put:
        #             pos.BTO(Put_Option(leg.strike, leg.current_value))
        #     elif leg.type == "SHORT":
        #         if type(leg) == ops.Call:
        #             pos.STO(Call_Option(leg.strike, leg.current_value))
        #         elif type(leg) == ops.Put:
        #             pos.STO(Put_Option(leg.strike, leg.current_value))
        # self.stats = pos
        for leg in self.stats.longs + self.stats.shorts:
            if leg.parent_pointer is option:
                leg.update_premium(Data)

        self.values["current value"] = self.stats.payoff_precise(stock_price_live(self.ticker))
