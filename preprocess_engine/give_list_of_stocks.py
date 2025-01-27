import pandas as pd

import yfinance as yf
import pandas as pd


# Load the CSV file into a DataFrame
file_path = 'nfourl_data.csv'  # Replace this with the correct path to your CSV file
df = pd.read_csv(file_path)

# Filter the rows where 'pInstType' is 'OPTSTK'
filtered_df = df[df['pInstType'] == 'OPTSTK']

# Get the unique 'pSymbolName' values as a list
fno_stocks = filtered_df['pSymbolName'].unique().tolist()

# Initialize an empty list to store stock data
stocks_in_range = []

# Define the price range
min_price = 2200
max_price = 3500

# Iterate over each F&O stock to check its current price
for stock in fno_stocks:
    try:
        # Fetch the stock data from yfinance
        stock_data = yf.Ticker(stock + ".NS")
        stock_price = stock_data.history(period="1d")['Close'].iloc[-1]
        
        # Check if the stock price is within the defined range
        if min_price <= stock_price <= max_price:
            stocks_in_range.append(stock)
    except Exception as e:
        print(f"Could not retrieve data for {stock}: {e}")


file_path_2 = 'nse_cm.csv'  # Replace with the correct path
df2 = pd.read_csv(file_path_2)
# Filter the rows where 'pGroup' is 'EQ' and 'pSymbolName' is in fno_stocks
df2_filtered = df2[(df2['pGroup'] == 'EQ') & (df2['pSymbolName'].isin(stocks_in_range))]

# Ensure 'pSymbolName' is unique, aggregating data if necessary
symbol_map = df2_filtered.set_index('pSymbolName')[['pSymbol', 'pTrdSymbol']].to_dict(orient='index')
# symbol_map = {'ADANIENT': {'pSymbol': 25, 'pTrdSymbol': 'ADANIENT-EQ'}, 'NAVINFLUOR': {'pSymbol': 14672, 'pTrdSymbol': 'NAVINFLUOR-EQ'}, 'ASIANPAINT': {'pSymbol': 236, 'pTrdSymbol': 'ASIANPAINT-EQ'}, 'BALKRISIND': {'pSymbol': 335, 'pTrdSymbol': 'BALKRISIND-EQ'}, 'COLPAL': {'pSymbol': 15141, 'pTrdSymbol': 'COLPAL-EQ'}, 'TVSMOTOR': {'pSymbol': 8479, 'pTrdSymbol': 'TVSMOTOR-EQ'}, 'GODREJPROP': {'pSymbol': 17875, 'pTrdSymbol': 'GODREJPROP-EQ'}, 'DEEPAKNTR': {'pSymbol': 19943, 'pTrdSymbol': 'DEEPAKNTR-EQ'}, 'GRASIM': {'pSymbol': 1232, 'pTrdSymbol': 'GRASIM-EQ'}, 'HINDUNILVR': {'pSymbol': 1394, 'pTrdSymbol': 'HINDUNILVR-EQ'}, 'M&M': {'pSymbol': 2031, 'pTrdSymbol': 'M&M-EQ'}, 'PIDILITIND': {'pSymbol': 2664, 'pTrdSymbol': 'PIDILITIND-EQ'}, 'RELIANCE': {'pSymbol': 2885, 'pTrdSymbol': 'RELIANCE-EQ'}, 'TITAN': {'pSymbol': 3506, 'pTrdSymbol': 'TITAN-EQ'}, 'TORNTPHARM': {'pSymbol': 3518, 'pTrdSymbol': 'TORNTPHARM-EQ'}, 'INDIAMART': {'pSymbol': 10726, 'pTrdSymbol': 'INDIAMART-EQ'}, 'SHRIRAMFIN': {'pSymbol': 4306, 'pTrdSymbol': 'SHRIRAMFIN-EQ'}, 'MPHASIS': {'pSymbol': 4503, 'pTrdSymbol': 'MPHASIS-EQ'}, 'LALPATHLAB': {'pSymbol': 11654, 'pTrdSymbol': 'LALPATHLAB-EQ'}}
print(symbol_map)
tokens = [
    {"instrument_token": str(details['pSymbol']), "exchange_segment": "nse_cm"}
    for symbol_name, details in symbol_map.items()
]
              
print(tokens)
print(len(symbol_map))
# Create a DataFrame from the filtered stocks
df = pd.DataFrame(stocks_in_range)

# Save the DataFrame to an Excel file
df.to_excel('fno_stocks_2500_to_3500.xlsx', index=False)

# print(f"Excel sheet created with {len(df)} stocks in the price range ₹{min_price} to ₹{max_price}.")
