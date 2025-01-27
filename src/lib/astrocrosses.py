import yfinance as yf
from datetime import datetime, timedelta

today = datetime.now()
previous_day_date = today - timedelta(days=1)
# Function to perform analysis on a single stock
def analyze_stock(ticker,astro_levels,level_movement):
    # Fetch the data for the stock
    stock_data = yf.Ticker(f"{ticker[:-3]}.NS")
    
    # Fetch historical data for the last 5 days to ensure we cover weekends and holidays
    hist = stock_data.history(period="5d")
    
    previous_trading_day = hist.index[hist.index.date <= previous_day_date.date()][-1]
    previous_day = hist.loc[previous_trading_day]
    
    # Extract the high and low points
    high_price = previous_day['High']
    low_price = previous_day['Low']
    
    # Determine how many astro levels the high and low have crossed
    crossed_levels = [level for level in astro_levels if low_price <= level <= high_price]
      
    # Find the row corresponding to the previous trading day
    # if previous_day_date.date() in hist.index.date:
    #     previous_day = hist[hist.index.date == previous_day_date.date()].iloc[0]
        
    #     # Extract the high and low points
    #     high_price = previous_day['High']
    #     low_price = previous_day['Low']
        
    #     # Determine how many astro levels the high and low have crossed
    #     crossed_levels = [level for level in astro_levels if low_price <= level <= high_price]
        
    if  len(crossed_levels) >= level_movement:
        return True
    else:
        return False

