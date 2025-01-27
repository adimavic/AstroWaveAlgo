import json
import pandas as pd

def change_strike(price, stock_name, option_data):
    # Flatten the JSON data
    all_data = [item for sublist in option_data.values() for item in sublist if item['pSymbolName'] == stock_name]
    
    # Convert the flattened data to a pandas DataFrame
    df = pd.DataFrame(all_data)
    
    if 'dStrikePrice;' in df.columns:
        df['dStrikePrice;'] = df['dStrikePrice;'].astype(float)
    
    # Find the closest strike price
    closest_strike = min(df['dStrikePrice;'], key=lambda x: abs(x - float(price)))
    
    # Get the trading symbol, lot size, and pSymbol for the closest strike price
    closest_row = df.loc[df['dStrikePrice;'] == closest_strike]
    trading_symbol = str(closest_row['pTrdSymbol'].iloc[0])
    lLotSize = closest_row['lLotSize'].iloc[0]
    pSymbol = str(closest_row['pSymbol'].iloc[0])
    
    return trading_symbol, lLotSize, pSymbol

# Load the data from the JSON files
# with open('ce_options.json', 'r') as f_ce:
#     ce_option_data = json.load(f_ce)

# with open('pe_options.json', 'r') as f_pe:
#     pe_option_data = json.load(f_pe)

# # Example usage:
# price = 2905  # Example price
# stock_name = "RELIANCE"  # Specific stock

# trading_symbol_ce, lLotSize_ce, pSymbol_ce = change_strike(price, stock_name, ce_option_data)
# trading_symbol_pe, lLotSize_pe, pSymbol_pe = change_strike(price, stock_name, pe_option_data)

# print("CE Data:")
# print("Trading Symbol CE:", trading_symbol_ce)
# print("Lot Size CE:", lLotSize_ce)
# print("pSymbol CE:", pSymbol_ce)

# print("\nPE Data:")
# print("Trading Symbol PE:", trading_symbol_pe)
# print("Lot Size PE:", lLotSize_pe)
# print("pSymbol PE:", pSymbol_pe)
