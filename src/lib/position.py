from datetime import datetime, timedelta
from tradingview_ta import TA_Handler, Interval, Exchange
import yfinance as yf

class TradePosition():
    def __init__(self,price,symbols,shape,astro_level,data):
        self.sym = symbols
        self.shape = shape
        self.price = price
        self.astro = astro_level
        self.data = data

    def get_target(self,level_name):
        if self.sym["position"] == "buy":
            index = self.astro.index(self.sym["target_level"])
            x5 = self.astro[index -1]
            fibo = self.sell_fibo_levels(self.sym["target_level"], x5)
            level_value = fibo.get(level_name.upper())
            if self.price >= level_value:
                return "target_achived"
        if self.sym["position"] == "sell":
            index = self.astro.index(self.sym["target_level"])
            x5 = self.astro[index + 1]
            fibo = self.buy_fibo_levels(self.sym["target_level"], x5)
            level_value = fibo.get(level_name.upper())
            if self.price <= level_value:
                return "target_achived"

    def take_trades(self):
        if self.shape["volume"] == True and None in(self.shape["trade"]["buy"],self.shape["trade"]["sell"]):
            if  self.sym["position"] == None:
                if self.price > self.shape["high"]:
                    return "buy"
                elif self.price < self.shape["low"]:
                    return "sell"
            
            if self.sym["position"] != None and self.sym["pyramid"] is True:
                if self.price > self.shape["high"]:
                    return "buy"
                elif self.price < self.shape["low"]:
                    return "sell"  

    def stopout(self):
        current_time = datetime.now()
        stoploss_counter = self.shape["trade"]["stoploss_counter"]

        if isinstance(stoploss_counter, str):
            stoploss_counter = datetime.strptime(stoploss_counter.split('.')[0], "%Y-%m-%d %H:%M:%S")
        if self.sym["position"] == "buy" and self.shape["volume"] == True:
            if self.price < self.shape["low"]:
                if stoploss_counter is None:
                    self.shape["trade"]["stoploss_counter"] = current_time
                    stoploss_counter = self.shape["trade"]["stoploss_counter"]
                if current_time > stoploss_counter + timedelta(seconds=self.data["sl_time"]):
                    if self.shape["trade"]["buy"] is True:
                        return "stoploss"
                    else: 
                        return "trailing_stoploss"
            else:
                 self.shape["trade"]["stoploss_counter"] = None

        if self.sym["position"] == "sell" and self.shape["volume"] == True:
            if self.price > self.shape["high"]:
                if stoploss_counter is None:
                    self.shape["trade"]["stoploss_counter"] = current_time
                    stoploss_counter = self.shape["trade"]["stoploss_counter"]
                if current_time > stoploss_counter + timedelta(seconds=self.data["sl_time"]):
                    if self.shape["trade"]["sell"] is True:
                        return "stoploss"
                    else: 
                        return "trailing_stoploss"
            else:
                 self.shape["trade"]["stoploss_counter"] = None

    def sell_fibo_levels(self, x2, x1):
        # Calculate Fibonacci levels and return them
        fib_levels = {
            "RED": x1 + (x2 - x1) * 0.382,
            "GOLD": x1 + (x2 - x1) * 0.50,
            "GREEN": x1 + (x2 - x1) * 0.618,
            "BLUE": x1 + (x2 - x1) * 0.786,
            "PURPLE": x1 + (x2 - x1) * (-0.27),
            "HGOLD": x1 + (x2 - x1) * (-0.618),
            "YELLOW": x1 + (x2 - x1) * 0.236
        }
        return fib_levels
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

    
    def get_sma(self,period, symbol):

        try:
            handler = TA_Handler(
                symbol=symbol,
                screener="india",
                exchange="NSE",
                interval=Interval.INTERVAL_1_MINUTE
            )
            analysis = handler.get_analysis()
            sma_value = analysis.indicators[f"SMA{period}"]
            return sma_value
        except Exception as e:
            return None  # Return None to indicate failure

    def find_crossover_level(self, symbol):
        # Fetch historical data for the last 200 minutes
        data = yf.download(tickers=symbol, period="5d", interval="1m")

        # Calculate the 50-period and 200-period SMA
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        data['SMA200'] = data['Close'].rolling(window=200).mean()

        # Identify the crossover points
        crossover = data[(data['SMA50'] > data['SMA200']) & (data['SMA50'].shift(1) < data['SMA200'].shift(1))]
        # Get the last crossover point
        if not crossover.empty:
            last_crossover = crossover.iloc[-1]
            crossover_price = last_crossover['SMA50']
            # Here you can map the crossover price to your astro levels
            crossover_level = self.map_to_astro_level(crossover_price)
            return crossover_level
        else:
            return None
 
    def map_to_astro_level(self, price):
        # Implement logic to map a price to the closest astro level
        closest_level = min(self.astro, key=lambda x: abs(x - price))
        return closest_level
    
    def target(self,trade):

        index = self.astro.index(self.shape["level"])
        # Get SMA values using TradingView
        target_level = None 
        if trade == "buy" and self.sym['totrade'] == True:
            sma_50 = self.get_sma(50,self.sym["key_tv"])
            sma_200 = self.get_sma(200,self.sym["key_tv"])
            if not None in(sma_50,sma_200)  and sma_50 < sma_200:
                # Fresh trade, target as usua
                    target_index = index + self.data["target"]
                    target_level = self.astro[target_index]
            else:
                # Late trade, adjust the target
                crossover_level = self.find_crossover_level(self.sym["key_yf"])

                if crossover_level is not None:
                    crossover_index = self.astro.index(crossover_level)
                    target_index = crossover_index +  self.data["target"]  # Adjust as per your strategy
                    target_level = self.astro[target_index]
                    if self.shape["level"] > target_level:
                        target_index = index + self.data["target"]
                        target_level = self.astro[target_index]
                else:
                    target_index = index + self.data["target"]
                    target_level = self.astro[target_index]
                    print("No recent crossover found.")
            self.sym["target_level"] = target_level
            return target_level
        elif trade == "sell" and self.sym['totrade'] == True:

            sma_50 = self.get_sma(50,self.sym["key_tv"])
            sma_200 = self.get_sma(200,self.sym["key_tv"])
            if not None in(sma_50,sma_200) and sma_50 > sma_200:
                target_index = index - self.data["target"]
                target_level = self.astro[target_index]
            else:
                # Late trade, adjust the target
                crossover_level = self.find_crossover_level(self.sym["key_yf"])
                if crossover_level is not None:
                    crossover_index = self.astro.index(crossover_level)
                    target_index = crossover_index - self.data["target"]  # Adjust as per your strategy
                    target_level = self.astro[target_index]
                    if self.shape["level"] < target_level:
                        target_index = index - self.data["target"]
                        target_level = self.astro[target_index]
                else:
                    target_index = index + self.data["target"]
                    target_level = self.astro[target_index]
                    print("No recent crossover found.")

            self.sym["target_level"] = target_level
            return target_level
