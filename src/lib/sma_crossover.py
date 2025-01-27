from datetime import datetime, timedelta
from tradingview_ta import TA_Handler, Interval

class SMACrossoverChecker:
    def __init__(self, symbols):
        self.symbols = symbols
        self.data = {symbol: {"sma50": [], "sma200": []} for symbol in symbols}
        self.bcg_up = False
        self.bcg_down = False
        self.ma_crossing = 0
        self.last_check_time = datetime.now()

    def fetch_sma(self, symbol):
        """Fetch SMA 50 and SMA 200 from TradingView for a given symbol."""
        handler = TA_Handler(
            symbol=symbol,
            screener="india",  # Assuming Indian market, change if different
            exchange="NSE",    # National Stock Exchange
            interval=Interval.INTERVAL_1_MINUTE  # 1-minute interval
        )
        analysis = handler.get_analysis()
        sma_50 = analysis.indicators['SMA50']
        sma_200 = analysis.indicators['SMA200']
        return sma_50, sma_200

    def update_sma_values(self):
        """Fetch and store the last 2 SMA values for each symbol."""
        for symbol in self.symbols:
            sma_50, sma_200 = self.fetch_sma(symbol)

            # Store the last 2 values
            self.data[symbol]["sma50"].append(sma_50)
            self.data[symbol]["sma200"].append(sma_200)

            # Keep only the last 2 values
            if len(self.data[symbol]["sma50"]) > 2:
                self.data[symbol]["sma50"].pop(0)
            if len(self.data[symbol]["sma200"]) > 2:
                self.data[symbol]["sma200"].pop(0)

    def check_crossover(self):
        """Check for SMA crossover for all symbols."""
        for symbol, sma_data in self.data.items():
            try:
                sma_50 = sma_data["sma50"]
                sma_200 = sma_data["sma200"]

                if len(sma_50) == 2 and len(sma_200) == 2:
                    # Check if SMA 50 crossed SMA 200 upwards
                    if sma_50[-1] > sma_200[-1] and sma_50[-2] <= sma_200[-2]:
                        self.bcg_up = True
                        self.ma_crossing += 1
                        print(f"{symbol}: SMA 50 crossed above SMA 200 (Up)")

                    else:
                        self.bcg_up = False

                    # Check if SMA 50 crossed SMA 200 downwards
                    if sma_50[-1] < sma_200[-1] and sma_50[-2] >= sma_200[-2]:
                        self.bcg_down = True
                        self.ma_crossing += 1
                        print(f"{symbol}: SMA 50 crossed below SMA 200 (Down)")

                    else:
                        self.bcg_down = False

            except Exception as e:
                print(f"Error checking crossover for {symbol}: {e}")

    def run(self):
        """Run the SMA update and crossover check every minute using datetime."""
        while True:
            current_time = datetime.now()

            # Check if 1 minute has passed since the last check
            if current_time >= self.last_check_time + timedelta(minutes=1):
                print(f"Running at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

                # Update the SMA values for all symbols
                self.update_sma_values()

                # Check for crossovers
                self.check_crossover()

                # Update the last check time
                self.last_check_time = current_time

# List of symbols you want to monitor
symbols = ["RELIANCE-EQ", "COLPAL-EQ"]

# Initialize the checker
checker = SMACrossoverChecker(symbols)

# Start the checking process
checker.run()
