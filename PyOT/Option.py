import datetime
from PyOT.Data.Market_Quotes import get_option_value


class indiv_option:
    # ticker is string, strike is float, type is string "CALL" or "PUT", expir_date is datetime, premium is float, create_date is datetime, deb_or_cred is "CREDIT" or "DEBIT"
    def __init__(self, ticker, strike, type, expir_date, initial_premium=None, create_date=None):
        self.TICKER = ticker
        self.strike = strike
        self.type = type.upper()
        self.create_date = create_date
        self.initial_premium = initial_premium if initial_premium is not None else get_option_value(
            ticker, strike, expir_date.strftime("%m/%d/%Y"), type)
        self.current_value = self.initial_premium
        self.expir_date = expir_date if not isinstance(
            expir_date, str) else datetime.strptime(expir_date, "%B %d, %Y")

    def __repr__(self):
        return "{} {} {} {} AT ${}".format(self.TICKER, self.expir_date.strftime("%m/%d/%Y"), self.strike, self.type, self.current_value)

    def update_value(self):
        self.current_value = get_option_value(
            self.TICKER, self.strike, self.expir_date, self.type)
        return self.current_value
