from PyOT.Data.profitnloss import *


class Positions:
    def __init__(self, legs=None, name=""):
        self.name = name
        self.legs = [] if legs is None else legs
        self.values = {"initial value": 0, "current value": 0}
        self.pnl = None
        self.ticker = ""
        self.stats = {}

    def add_leg(self, option_tuple):
        self.legs.append(option_tuple)

    def initialize(self):
        pos = Strategy()
        for leg in self.legs:
            if leg[1] == "DEBIT":
                if leg[0].type == "CALL":
                    pos.buy(Call(leg[0].strike, leg[0].initial_premium))
                if leg[0].type == "PUT":
                    pos.buy(Put(leg[0].strike, leg[0].initial_premium))
            if leg[1] == "CREDIT":
                if leg[0].type == "CALL":
                    pos.sell(Call(leg[0].strike, leg[0].initial_premium))
                if leg[0].type == "PUT":
                    pos.sell(Put(leg[0].strike, leg[0].initial_premium))
        self.pnl = pos

        # Could replace this with a function provided by profitnloss?
        for leg in self.legs:
            if leg[1] == "DEBIT":
                self.values["initial value"] -= leg[0].current_value
            elif leg[1] == "CREDIT":
                self.values["initial value"] += leg[0].current_value
        self.values["current value"] = self.values["initial value"]

        if len(self.legs) > 0:
            self.ticker = self.legs[0][0].TICKER

        self.stats.update({"Break evens": pos.break_evens(
        ), "Max profit": pos.max_gain(), "Max loss": pos.max_loss()})

    def __repr__(self):
        return "{} {} worth ${}".format(self.ticker, self.name, self.values["current value"])

    def refresh_value(self):
        self.values["current value"] = 0
        for leg in self.legs:
            if leg[1] == "DEBIT":
                self.values["current value"] -= leg[0].current_value
            elif leg[1] == "CREDIT":
                self.values["current value"] += leg[0].current_value
        return self.values["current value"]
