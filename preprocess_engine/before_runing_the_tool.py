import json
from datetime import datetime
import os

def read_existing_config(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {
        "startAt": "9:15",
        "endAt": "2:59",
        "exitAt": 0,
        "capital": 50000,
        "cap_utized":0,
        "total": 44,
        "closing_time": 70,
        "sl_time": 20,
        "target": 4,
        "debug": False,
        "symbols": []
        }

def generate_stock_config(symbols, file_path):
    stock_config = read_existing_config(file_path)
    existing_keys = {symbol["key"] for symbol in stock_config["symbols"]}

    for symbol in symbols:
        for key, value in symbol.items():
            if key not in existing_keys:
                key_yf = key[:-3] + ".NS"
                stock_data = {
                    "key": key, # her the key is 
                    "key_yf": key_yf,
                    "key_tv": key[:-3],
                    "instrument_token":value,
                    "totrade": None,
                    "pyramid": None,
                    "lotsize": None,
                    "position": None,
                    "target_level": None,
                    "price_list": [
                    ],
                    "crossed_levels": [
                    ],
                    "detected_level": None,
                    "shapes": [
                    ]
                }
                stock_config["symbols"].append(stock_data)

    stock_config["total"] = len(stock_config["symbols"])

    return json.dumps(stock_config, indent=4)

# Example usage
symbols = [{'HINDUNILVR-EQ': '1394'}, {'TVSMOTOR-EQ': '8479'}, {'PIDILITIND-EQ': '2664'}, {'RELIANCE-EQ': '2885'}, {'INDIAMART-EQ': '10726'}, {'SHRIRAMFIN-EQ': '4306'}, {'MPHASIS-EQ': '4503'}, {'ACC-EQ': '22'}, {'ASIANPAINT-EQ': '236'}, {'BALKRISIND-EQ': '335'}, {'GRASIM-EQ': '1232'}, {'SRF-EQ': '3273'}, {'ADANIENT-EQ': '25'}, {'M&M-EQ': '2031'}, {'NAVINFLUOR-EQ': '14672'}, {'GODREJPROP-EQ': '17875'}, {'NESTLEIND-EQ': '17963'}, {'COLPAL-EQ': '15141'}, {'TITAN-EQ': '3506'}, {'TORNTPHARM-EQ': '3518'}, {'DEEPAKNTR-EQ': '19943'}, {'LALPATHLAB-EQ': '11654'}]

file_path = 'stock_config.json'
json_data = generate_stock_config(symbols, file_path)

# Optionally, write to a file
with open(file_path, 'w') as file:
    file.write(json_data)

print(json_data)
