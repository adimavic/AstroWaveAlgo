from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

class touchandgo_Down:
    def __init__(self, json_data):
        self.data = json_data
        self.symbols = self.data["symbols"]
        self.closingtime = self.data["closing_time"]  

    def buy_fibo_levels(self, x1, x2):
        # Calculate Fibonacci levels and return them
        fib_levels = {
            "RED": x2 - (x2 - x1) * 0.382,
            "GOLD": x2 - (x2 - x1) * 0.50,
            "GREEN": x2 - (x2 - x1) * 0.618,
            "BLUE": x2 - (x2 - x1) * 0.786,
            "PURPLE": x2 - (x2 - x1) * (-0.27),
            "HGOLD": x2 - (x2 - x1) * (-0.618),
            "YELLOW": x2 - (x2 - x1) * 0.236
        }
        return fib_levels

    def make_shape_sell(self, symbol, price):
        current_time = datetime.now()
        for sym in self.symbols:
            if sym["key"] == symbol:
                for level in sym["shapes"]:
                    if sym["detected_level"] == level["level"] and sym["totrade"] == True:
                        shape = level
                        if shape["shape_buy"] is not True :
                            if float(price) < shape["level"] and shape["shape_sell"] is not True:
                                if shape["shape_buy"] == None:
                                    shape["shape_sell"] = "inprogress"
                                if shape["shapetime"] is None:
                                    shape["shapetime"] = current_time
                                if len(shape["shape"]) == 0:
                                    shape["shape"].append(float(price))
                                else:
                                    high = max(shape["shape"])
                                    low = min(shape["shape"])
                                    if float(price) < low:
                                        shape["shape"] = [high, float(price)]
                                    elif float(price) > high:
                                        shape["shape"] = [float(price), low]


                            if shape["shapetime"] is not None:
                                if isinstance(shape["shapetime"], str):
                                    shapetime_dt = datetime.strptime(shape["shapetime"], "%Y-%m-%d %H:%M:%S")
                                else:
                                    shapetime_dt = shape["shapetime"]

                                elapsed_time = (current_time - shapetime_dt).total_seconds()

                                if elapsed_time < self.closingtime and float(price) >= shape["level"] and shape["shape_sell"] == "inprogress":
                                    shape["shape"] = []
                                    shape["shapetime"] = None
                                    shape["shape_sell"] = None

                                if elapsed_time >= self.closingtime and float(price) >= shape["level"] and shape["shape_sell"] == "inprogress":
                                    if  shape["shape_sell"] != True:
                                        print((sym["key_yf"], shape["level"], shapetime_dt.strftime("%Y-%m-%d %H:%M:%S"), current_time.strftime("%Y-%m-%d %H:%M:%S")))
                                        verification = self.verify_closing(sym["key_yf"], shape["level"], shapetime_dt.strftime("%Y-%m-%d %H:%M:%S"), current_time.strftime("%Y-%m-%d %H:%M:%S"))
                                        if verification == True:
                                            shape["shape_sell"] = True
                                        elif verification == False:
                                            shape["shape"] = []
                                            shape["shapetime"] = None
                                            shape["low"] = None
                                            shape["high"] = None
                                            shape["shape_sell"] = None

                                if shape["shape_sell"] == True and shape["status"] == None:
                                    high = max(shape["shape"])
                                    low = min(shape["shape"])
                                    if float(price) > high:
                                        shape["shape"] = [float(price), low]
                                    elif float(price) < low:
                                        shape["shape"] = [high, float(price)]
                                    shape["high"] = max(shape["shape"])
                                    shape["low"] = min(shape["shape"])

    def reverse_sell(self, symbol, price, level_name):
        for sym in self.symbols:
            if sym["key"] == symbol:
                for level in sym["shapes"]:
                    if sym["detected_level"] == level["level"] and sym["totrade"] == True:
                        shape = level
                        if shape["shape_sell"] == True:
                            fib_levels = self.buy_fibo_levels(shape["low"], shape["high"])
                            level_value = fib_levels.get(level_name.upper())
                            if float(price) < level_value and float(price) > shape["low"]:
                                print(f"Thinking of reversal for {symbol}")
                                if shape["endshapetime"] == None and shape["status"] == None:
                                    shape["endshapetime"] = datetime.now()
                                    shape["status"] = "completed"

    def verify_closing(self, ticker, level, startshapetime, endshapetime):
        if self.data["debug"] == True:
            return True
        # return True

        if isinstance(startshapetime, str):
            start_time = datetime.strptime(startshapetime.split('.')[0], "%Y-%m-%d %H:%M:%S")
        if isinstance(endshapetime, str):
            end_time = datetime.strptime(endshapetime.split('.')[0], "%Y-%m-%d %H:%M:%S")
            
        time_diff = end_time - start_time
        if time_diff < timedelta(minutes=2):
            return False
        # Subtract 1 minute from the end time
        end_time -= timedelta(minutes=1)

        start_time = pd.to_datetime(startshapetime)
        end_time = pd.to_datetime(endshapetime)

        try:
            data = yf.download(tickers=ticker, period='5d', interval='1m')

            # Ensure the index is a DatetimeIndex
            if not isinstance(data.index, pd.DatetimeIndex):
                raise ValueError("Data index is not a DatetimeIndex. Cannot apply tz_localize.")

            # Ensure index is naive datetime
            data.index = data.index.tz_localize(None)

        except Exception as e:
            return False

        # Filter data between the start and end times
        filtered_data = data[(data.index >= start_time) & (data.index <= end_time)]

        both_below_level = ((filtered_data['High'] < level) & (filtered_data['Low'] < level)).any()

        # print(f"Data between {startshapetime} and {endshapetime}:")
        # print(filtered_data)
        # print(f"At least one candle with both high and low prices below {level}: {both_below_level}")

        return both_below_level
