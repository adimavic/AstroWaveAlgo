import os
import json
import pandas as pd

def make_data(stock_names, file_path_PE, file_path_CE):
    try:
        if os.path.isfile(file_path_CE):
            os.remove(file_path_CE)
        if os.path.isfile(file_path_PE):
            os.remove(file_path_PE)
    except Exception as e:
        print(f"Error while removing files: {e}")

    # Load the data from the CSV file
    csv_file_path = 'nse_fo_spt.csv'
    fnodf = pd.read_csv(csv_file_path)
    fnodf.columns = [c.strip() for c in fnodf.columns.values.tolist()]

    if 'lExpiryDate' in fnodf.columns:
        fnodf['lExpiryDate'] = pd.to_datetime(fnodf['lExpiryDate'], unit='s')
        fnodf['lExpiryDate'] = (fnodf['lExpiryDate'] + pd.DateOffset(years=10)).dt.floor('D')
    else:
        print("Error: 'lExpiryDate' column not found in the DataFrame.")

    if 'dStrikePrice;' in fnodf.columns:
        fnodf['dStrikePrice;'] = fnodf['dStrikePrice;'].astype(str).str[:-4]
    else:
        print("Error with the strike price")

    expiry = input("Input the expiry date of option <2023-12-28><Years-Month-Date>")

    data_ce = {}
    data_pe = {}

    for stock in stock_names:
        # Extract stock name (key) from the dictionary
        stock_name = list(stock.keys())[0][:-3]
        filtered_ce = fnodf[(fnodf.pSymbolName == stock_name) & (fnodf.pOptionType == 'CE') & (fnodf.lExpiryDate == expiry)]
        filtered_pe = fnodf[(fnodf.pSymbolName == stock_name) & (fnodf.pOptionType == 'PE') & (fnodf.lExpiryDate == expiry)]
        
        selected_columns = ['pSymbol', 'pSymbolName', 'pOptionType', 'dStrikePrice;', 'pTrdSymbol','lLotSize']
        
        filtered_ce = filtered_ce[selected_columns]
        filtered_pe = filtered_pe[selected_columns]
        
        if stock_name not in data_ce:
            data_ce[stock_name] = []
        if stock_name not in data_pe:
            data_pe[stock_name] = []

        data_ce[stock_name].extend(filtered_ce.to_dict(orient='records'))
        data_pe[stock_name].extend(filtered_pe.to_dict(orient='records'))

    with open(file_path_CE, 'w') as f_ce:
        json.dump(data_ce, f_ce, indent=4)
    
    with open(file_path_PE, 'w') as f_pe:
        json.dump(data_pe, f_pe, indent=4)

# Example usage:
stock_names = [{'HINDUNILVR-EQ': 2722.05}, {'TVSMOTOR-EQ': 2605.5}, {'PIDILITIND-EQ': 3030.75},
               {'INDIAMART-EQ': 2673.35}, {'SHRIRAMFIN-EQ': 2895.1}, {'MPHASIS-EQ': 2718.85},
               {'RELIANCE-EQ': 2923.7}, {'ADANIENT-EQ': 3040.1}, {'ACC-EQ': 2281.95},
               {'ASIANPAINT-EQ': 3025.85}, {'GRASIM-EQ': 2512.4}, {'BALKRISIND-EQ': 2781.45},
               {'SRF-EQ': 2491.75}, {'M&M-EQ': 2745.25}, {'NAVINFLUOR-EQ': 3237.6},
               {'GODREJPROP-EQ': 2873.7}, {'NESTLEIND-EQ': 2474.6}, {'COLPAL-EQ': 3468.5},
               {'TITAN-EQ': 3402.15}, {'TORNTPHARM-EQ': 3348.75}, {'DEEPAKNTR-EQ': 2846.65},
               {'LALPATHLAB-EQ': 3207.8}]
file_path_PE = 'pe_options.json'
file_path_CE = 'ce_options.json'

make_data(stock_names, file_path_PE, file_path_CE)
