import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class VolumeAnalyser:
    def __init__(self, json_data):
        self.data = json_data
        self.symbols = self.data["symbols"]

    def fetch_data(self, ticker, period='5d', interval='1m'):
        data = yf.download(tickers=ticker, period=period, interval=interval)
        return data

    def calculate_sma(self, data, window):
        return data.rolling(window=window).mean()

    def analyze_volume(self, ticker, start_time, end_time, volume_threshold=0.1):
        if self.data["debug"] == True:
            return True

        # Convert the input strings to datetime objects
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time.split('.')[0], "%Y-%m-%d %H:%M:%S")
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time.split('.')[0], "%Y-%m-%d %H:%M:%S")
           
        next_minute = end_time + timedelta(minutes=1)
        next_minute = next_minute.replace(second=0, microsecond=0)
        try:
            if datetime.now() > next_minute:
            # Remove fractional seconds by setting seconds and microseconds to zero
                start_datetime = start_time.replace(second=0, microsecond=0)
                end_datetime = end_time.replace(second=0, microsecond=0)
                data = self.fetch_data(ticker)
                # Ensure the timestamps are naive (timezone-unaware)
                data.index = data.index.tz_localize(None)

                total_time = end_datetime - start_datetime
                calc_sma_from_time = start_datetime - total_time

                market_open_time = start_datetime.replace(hour=9, minute=15)
                market_close_time = start_datetime.replace(hour=15, minute=30)
                
                # If the start time of the SMA calculation is before the market opens, adjust it
                if calc_sma_from_time < market_open_time:
                    previous_day_minutes = (market_open_time - calc_sma_from_time).seconds // 60
                    
                    # Pull data from the previous day's closing period
                    previous_day_close_time = market_close_time - timedelta(days=1)
                    calc_sma_from_time = previous_day_close_time - timedelta(minutes=previous_day_minutes)
                    
                    # Combine previous day's data with current day
                    previous_day_data = data.loc[calc_sma_from_time:previous_day_close_time]
                    current_day_data = data.loc[market_open_time:end_datetime]
                    filtered_data = pd.concat([previous_day_data, current_day_data])
                else:
                    filtered_data = data.loc[calc_sma_from_time:end_datetime].copy()

                # Calculate SMA for the total time window
                sma_window = int(total_time.total_seconds() // 60) + 1 # SMA window in minutes
                filtered_data['SMA'] = self.calculate_sma(filtered_data['Volume'], sma_window)

                # Get start and end SMA values
                start_sma = filtered_data.loc[start_datetime]['SMA']
                end_sma = filtered_data.loc[end_datetime]['SMA']

                # Check if SMA increased by more than 0.5%
                sma_increase = ((end_sma - start_sma) / start_sma) * 100 > volume_threshold
                volume_crossed_sma = ((filtered_data['Volume'] - filtered_data['SMA']) / filtered_data['SMA'] * 100 > volume_threshold).any()
                if sma_increase and volume_crossed_sma:
                    return True
                else:
                    return True
        except:
            return True

