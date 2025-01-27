"Will be used to detect teh levels"

def detect_price_levels(prices, astro_level, data):
    if 'symbols' not in data:
        print("Error: 'symbols' key not found in JSON data.")
        return

    for stock_price in prices:
        for stock, price in stock_price.items():
            # Check if stock is present in the data
            stock_data = next((symbol for symbol in data['symbols'] if symbol.get('key') == stock), None)
            if stock_data is None:
                print(f"Stock {stock} not found in JSON file.")
                continue

            price_list = stock_data.get('price_list', [])
            crossed_levels = stock_data.get('crossed_levels', [])
            shapes = stock_data.get('shapes', [])

            # Update price list
            price_list.append(price)
            if len(price_list) > 2:
                price_list.pop(0)

            state = {
                "price_list": price_list,
                "crossed_levels": crossed_levels,
                "detected_level": stock_data.get("detected_level", None),
                "shapes": shapes
            }
            new_level_detected = False
            if len(price_list) > 1:
                for level in astro_level:
                    if price_list[-1] > level and price_list[-2] <= level:
                        state["detected_level"] = level
                        new_level_detected = True
                        if level not in state["crossed_levels"]:
                            state["crossed_levels"].append(level)
                        state["crossed_levels"] = sorted(list(set(state["crossed_levels"])), key=lambda x: state["crossed_levels"].index(x))
                        break
                    if price_list[-1] < level and price_list[-2] >= level:
                        state["detected_level"] = level
                        new_level_detected = True
                        if level not in state["crossed_levels"]:
                            state["crossed_levels"].append(level)
                        state["crossed_levels"] = sorted(list(set(state["crossed_levels"])), key=lambda x: state["crossed_levels"].index(x))
                        break

            detected_level = state["detected_level"]
            if detected_level is not None:
                if not any(shape["level"] == detected_level for shape in shapes):
                    for symbol in data["symbols"]:
                        if symbol["key"] == stock:
                            shapes = symbol["shapes"]
                            for i in range(len(shapes) - 1, -1, -1):
                                if not shapes[i].get("volume"):
                                    shapes.pop(i)

                    new_shape = {
                        "level": detected_level,
                        "shape": [],
                        "shape_buy": None,
                        "shape_sell": None,
                        "volume": None,
                        "low": None,
                        "high": None,
                        "status": None,
                        "shapetime": None,
                        "endshapetime": None,
                        "trade": {
                            "option_token": None,
                            "option_symbol": None,
                            "lotsize": None,
                            "buy": None,
                            "sell": None,
                            "stoploss_counter": None,
                            "sl_no": 0
                        }
                    }
                    shapes.append(new_shape)

            # Update JSON data
            for symbol in data['symbols']:
                if symbol.get('key') == stock:
                    symbol.update(state)
                    break
