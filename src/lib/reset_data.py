import json

class SymbolDataManager:
    def __init__(self, data):
        self.data = data

    def clear_data_on_tl(self, symbol_key):
        # Iterate over symbols and clear data for the specified symbol
        #After hitting the traget
        for symbol in self.data["symbols"]:
            if symbol["key"] == symbol_key:
                symbol["totrade"] = None
                symbol["pyramid"] = None
                symbol["lotsize"] = None
                symbol["position"] = None
                symbol["target_level"] = None
                symbol["price_list"] = []
                symbol["crossed_levels"] = []
                symbol["detected_level"] = None
                symbol["shapes"] = []
                break

    def clear_data_on_sl(self, symbol_key, target_level):
        # Iterate over symbols and find the one matching the symbol_key
        for symbol in self.data["symbols"]:
            if symbol["key"] == symbol_key:
                # Filter shapes to keep only the one with the target level
                symbol["shapes"] = [shape for shape in symbol["shapes"] if shape["level"] == target_level]
                break

    def get_data(self):
        return self.data


# Create an instance of SymbolDataManager
# manager = SymbolDataManager(json_data)

# # Clear shapes except the specified level
# manager.clear_shape("HINDUNILVR-EQ", 2929.515625)

# # Get the updated data
# updated_data = manager.get_data()

# # Print the updated JSON data
# print(json.dumps(updated_data, indent=4))
