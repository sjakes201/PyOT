from PyOT.Data.Market_Quotes import *
from PyOT.Option import indiv_option
from PyOT.Positions import Positions
import datetime

def test_valid_ticker():
    tickers = ["GOOG", "AAPL", "MSFT", "GOOGL", "AMZN", "SHW"]
    in_nasdaq_list = list(map(lambda symbol: valid_ticker(symbol), tickers))
    in_nasdaq_list.append(not valid_ticker("FAKETICKER"))
    print("test_valid_ticker contains valid tickers only: " + str(not (False in in_nasdaq_list)))


def test_live_price():
    try:
        TSLA_price = stock_price_live("TSLA")
        if(TSLA_price > 130 and TSLA_price < 135): #will need to have updated manually confirmed values for later tests
            print("stock_price_live correctly returns live price: True")
        else:
            print("lstock_price_live correctly returns live price: False")
    except:
        print("stock_price_live ERRORED in getting stock price")

def test_options_value():
    results = [] #will need to have updated manually confirmed values for later tests
    results.append(get_option_value("NKE", 120, "01/27/2023", "PUT") == 0.12)
    results.append(get_option_value("AAPL", 137, "01/27/2023", "PuT") == 1.56)
    results.append(get_option_value("META", 142, "02/03/2023", "CALL") == 7.0)
    results.append(get_option_value("META", 126, "02/03/2023", "Put") == 2.87)
    results.append(get_option_value("META", 127, "02/03/2023", "Put") == 3.2)
    results.append(get_option_value("META", 128, "02/03/2023", "Put") == 3.43)
    results.append(get_option_value("META", 129, "02/03/2023", "Put") == 3.77)
    results.append(get_option_value("META", 130, "02/03/2023", "Put") == 4.1)
    results.append(get_option_value("META", 131, "02/03/2023", "Put") == 4.29)
    print("get_option_value returns correct value: " + str(not False in results))

def test_indiv_option():
    apple = indiv_option("AAPL", 142, "CALL", datetime.datetime(2023, 2, 3))
    print(apple)



def test_basic_position_creation():
    appl1 = indiv_option("AAPL", 142, "CALL", datetime.datetime(2023, 2, 3))
    appl2 = indiv_option("AAPL", 144, "CALL", datetime.datetime(2023, 2, 3))
    appl3 = indiv_option("AAPL", 134, "PUT", datetime.datetime(2023, 2, 3))
    appl4 = indiv_option("AAPL", 132, "PUT", datetime.datetime(2023, 2, 3))
    iron_condor = Positions([(appl1, "CREDIT"), (appl2, "DEBIT"),(appl3, "CREDIT"), (appl4, "DEBIT")], "Iron Condor")
    spread = Positions([(appl1, "CREDIT"), (appl2, "DEBIT")], "Spread")
    spread.initialize()
    print(spread.values["current value"])
    iron_condor.initialize()
    print(iron_condor)
    print(iron_condor.stats)
    iron_condor.refresh_value()
    print(iron_condor)
    iron_condor.refresh_value()
    print(iron_condor)
    iron_condor.refresh_value()
    print(iron_condor)

test_basic_position_creation()


# test_valid_ticker()
# test_live_price()
# test_options_value()
# test_indiv_option()