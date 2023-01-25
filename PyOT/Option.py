import datetime
import PyOT.Data.Observers as obs
from PyOT.Data.Market_Quotes import get_option_value

class Call:
    def __init__(self, ticker, strike, expir_date, type, initial_premium=None, create_date=None):
        self.type = type
        self.TICKER = ticker
        self.strike = strike
        self.create_date = create_date
        self.initial_premium = self.current_value = initial_premium if initial_premium is not None else get_option_value(
            ticker, strike, expir_date.strftime("%m/%d/%Y"), self.__class__.__name__)
        self.expir_date = expir_date if not isinstance(
            expir_date, str) else datetime.strptime(expir_date, "%B %d, %Y")

        self.updater = obs.Publisher()

    def __repr__(self):
        return "{} {} {} {} AT ${}".format(self.TICKER, self.expir_date.strftime("%m/%d/%Y"), self.strike, self.__class__.__name__, self.current_value)

    def update_value(self):
        self.current_value = get_option_value(self.TICKER, self.strike, self.expir_date.strftime("%m/%d/%Y"), self.__class__.__name__)
        self.updater.publish(self, self.current_value)

    def MANUAL_UPDATE(self, prem):
        self.current_value = prem
        self.updater.publish(self, self.current_value)

class Put(Call):
    pass