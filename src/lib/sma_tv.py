from tradingview_ta import TA_Handler, Interval, Exchange

# Set up the handler for Reliance with a 1-minute interval
reliance = TA_Handler(
    symbol="RELIANCE",
    screener="india",
    exchange="NSE",
    interval=Interval.INTERVAL_1_MINUTE
)

# Fetch the analysis
analysis = reliance.get_analysis()

# Extract the 50 SMA and 200 SMA
sma_50 = analysis.indicators.get('SMA50', None)
sma_200 = analysis.indicators.get('SMA200', None)

print(f"50 SMA (1-min): {sma_50}")
print(f"200 SMA (1-min): {sma_200}")

import yfinance as yf
import pandas as pd

# Define the ticker symbol
ticker_symbol = "RELIANCE.NS"  # Use the appropriate symbol for NSE

# Download historical data for the specified interval
data = yf.download(ticker_symbol, start="2024-07-26 14:00:00", end="2024-07-26 14:10:00", interval="1m")

# Filter data between the specified time
data = data.between_time("14:00", "14:10")

# Calculate the 10-period SMA for volume
data['SMA10_Volume'] = data['Volume'].rolling(window=10).mean()

print("Filtered Volume Data:")
print(data[['Volume']])

print("\n10-Period SMA of Volume:")
print(data[['SMA10_Volume']])


