from PyOT.Data.Market_Quotes import *
from PyOT.Option import *
from PyOT.Position import Positions
import datetime
import PyOT.Event_Scheduler as EVENT
import threading

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
    op1 = Call("NOW", 480, datetime.datetime(2023, 2, 17), "SHORT")
    op2 = Call("NOW", 490, datetime.datetime(2023, 2, 17), "LONG")
    op3 = Put("NOW", 430, datetime.datetime(2023, 2, 17), "SHORT")
    op4 = Put("NOW", 420, datetime.datetime(2023, 2, 17), "LONG")
    pos = [op1,op2,op3,op4]
    iron_condor = Positions("Iron Condor")
    for p in pos:
        iron_condor.add_leg(p)
    print(iron_condor)
    # iron_condor.remove_leg(appl5)
    # print(iron_condor)
    print(iron_condor.values)
    # # appl1.MANUAL_UPDATE(appl1.current_value - 0.3)
    # # print(iron_condor.values)
    print(iron_condor.legs)

def test_update_mananger():
    op1 = Call("SHOP", 50, datetime.datetime(2023, 2, 17), "SHORT")
    op2 = Call("SHOP", 55, datetime.datetime(2023, 2, 17), "LONG")
    op3 = Put("SHOP", 35, datetime.datetime(2023, 2, 17), "SHORT")
    op4 = Put("SHOP", 30, datetime.datetime(2023, 2, 17), "LONG")
    # op5 = Call("SHOP", 50, datetime.datetime(2023, 2, 17), "SHORT")
    # op6 = Call("SHOP", 55, datetime.datetime(2023, 2, 17), "LONG")
    # op7 = Put("SHOP", 35, datetime.datetime(2023, 2, 17), "SHORT")
    # op8 = Put("SHOP", 30, datetime.datetime(2023, 2, 17), "LONG")
    double_condor = Positions("Iron Condor")
    ops = [op1,op2,op3,op4]
    for o in ops:
        double_condor.add_leg(o)
    # print(double_condor)
    # print(double_condor.values)
    print("Test")


op1 = Call("SHOP", 50, datetime.datetime(2023, 2, 17), "SHORT")
op2 = Call("SHOP", 55, datetime.datetime(2023, 2, 17), "LONG")
op3 = Put("SHOP", 35, datetime.datetime(2023, 2, 17), "SHORT")
op4 = Put("SHOP", 30, datetime.datetime(2023, 2, 17), "LONG")

EVENT.options_to_update.append(op1)
EVENT.options_to_update.append(op2)
EVENT.options_to_update.append(op3)
EVENT.options_to_update.append(op4)
best_pos = Positions("Iron Condor")
best_pos.add_leg(op1)
best_pos.add_leg(op2)
best_pos.add_leg(op3)
best_pos.add_leg(op4)

print(EVENT.options_to_update)
EVENT.start_jobs()
print("test after job start")