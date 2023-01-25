from yahoo_fin.stock_info import get_live_price
from yahoo_fin.options import get_calls, get_puts, get_expiration_dates
from datetime import datetime


def valid_ticker(ticker):
    try:
        get_live_price(ticker)
        return True
    except:
        return False


def stock_price_live(ticker):
    try:
        return get_live_price(ticker)
    except:
        return None


def get_expirations(ticker):
    expirs = get_expiration_dates(ticker)
    dates = list(
        map(lambda date: datetime.strptime(date, "%B %d, %Y"), expirs))
    return dates


def get_option_value(ticker, strike, expiration, type):
    expir = expiration if isinstance(expiration, str) else expiration.strftime("%d/%m/%Y")
    option_chain = None
    if type.upper() == "CALL":
        option_chain = get_calls(ticker, expir)
    if type.upper() == "PUT":
        option_chain = get_puts(ticker, expir)
    strikes = list(option_chain['Strike'])
    strike_index = strikes.index(strike)
    premium = option_chain['Last Price'][strike_index]
    return premium

