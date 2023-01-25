from PyOT.Data.Market_Quotes import *
from PyOT.Option import *
from PyOT.Position import Positions
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
    apple = Call("AAPL", 142, "CALL", datetime.datetime(2023, 2, 3))
    print(apple)



def test_basic_position_creation():
    appl1 = Call("AAPL", 148, datetime.datetime(2023, 2, 3), "SHORT")
    appl2 = Call("AAPL", 150, datetime.datetime(2023, 2, 3), "LONG")
    appl3 = Put("AAPL", 137, datetime.datetime(2023, 2, 3), "SHORT")
    appl4 = Put("AAPL", 135, datetime.datetime(2023, 2, 3), "LONG")
    pos = [appl1, appl2, appl3, appl4]
    iron_condor = Positions("Iron Condor")
    for p in pos:
        iron_condor.add_leg(p)
    iron_condor.initialize()
    print(iron_condor)
    print(iron_condor.values)
    appl1.MANUAL_UPDATE(appl1.current_value - 0.3)
    print(iron_condor.values)


test_basic_position_creation()


# test_valid_ticker()
# test_live_price()
# test_options_value()
# test_indiv_option()