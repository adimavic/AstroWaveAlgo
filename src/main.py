from neo_api_client import NeoAPI
from lib import configuration
from lib import astro_parser
from lib import touchdown
from lib import touchup
from lib import level_detector
from lib import sounds
from lib import position
from lib import astrocrosses
from lib import reset_data
from lib import validation
from lib import change_strike
from datetime import datetime
from lib import emial_alert
import traceback

def place_order(price,transaction_type,trading_symbol,QUANTITY,ORDERTYPE):
    if data["debug"] == False:
        try:
            resposne = client.place_order(exchange_segment='nse_cm', product=ORDERTYPE, price=price, order_type='MKT', 
                            quantity=QUANTITY, validity='DAY', trading_symbol=trading_symbol,
                            transaction_type=transaction_type, disclosed_quantity="0", market_protection="0")
            return resposne
        except Exception as e:
            return None

quantity = "1"
buffer = 2
def buy_ce(token): #{'stat': 'Ok', 'nOrdNo': '240813001947699', 'tid': 'server3_2983884', 'stCode': 200}

    #### The below code is used while placing the order for in options
    # trading_symbol_ce, lLotSize_ce, pSymbol_ce = change_strike.change_strike(price,stock[:-3],ce_data)
    # level["trade"]["option_token"] = pSymbol_ce
    # level["trade"]["option_symbol"] = trading_symbol_ce
    # level["trade"]["lotsize"] = int(lLotSize_ce)
    
    # print(trading_symbol_ce, lLotSize_ce, pSymbol_ce)
    if data["debug"] == True:
        return True
    margin_data = client.margin_required(exchange_segment="nse_cm", price=str(price), order_type="L", product="MIS", quantity=quantity, instrument_token=token, transaction_type="B")
    if isinstance(margin_data, dict) and "data" in margin_data and margin_data['data'].get('stCode') == 200:
        margin_required = float(margin_data['data']['ordMrgn'])
        level_range = level["high"] - level["low"]
        if  level_range <= 18 and (price - level["low"]) < (level_range + buffer) and float(margin_data['data']['avlCash']) > margin_required and (margin_required + data["cap_utized"]) < data["capital"] :
            place_new_order = place_order(str(price),"B",stock,quantity,"MIS")
            if isinstance(place_new_order, dict) and "stCode" in place_new_order and place_new_order.get("stCode")== 200:
                orderId = place_new_order['nOrdNo']
                executed = validate.wait_for_order_execution(stock,orderId, max_attempts=3)
                if executed is True:
                    data["cap_utized"] =  data["cap_utized"] + margin_required
                    print("buy CE,Going Up")
                    return True
                if executed is False:
                    cancellation = validate.cancel_and_check_order(orderId)
                    if cancellation is True:
                        return False
                    else:
                        cancellation = validate.cancel_and_check_order(orderId)
                        if cancellation is True:
                            return False
            else:
                return False
    # except:
    #     return None

def buy_pe(token): #{'stat': 'Ok', 'nOrdNo': '240813001947699', 'tid': 'server3_2983884', 'stCode': 200}
    # trading_symbol_pe, lLotSize_pe, pSymbol_pe = change_strike.change_strike(price,stock[:-3],pe_data)
    # print(trading_symbol_pe, lLotSize_pe, pSymbol_pe)
    if data["debug"] == True:
        return True
    margin_data = client.margin_required(exchange_segment="nse_cm", price=str(price), order_type="L", product="MIS", quantity=quantity, instrument_token=token, transaction_type="S")
    if isinstance(margin_data, dict) and "data" in margin_data and margin_data['data'].get('stCode') == 200:
        margin_required = float(margin_data['data']['ordMrgn'])
        level_range = level["high"] - level["low"]
        if  level_range <= 18 and (level["high"] - price) < (level_range + buffer) and float(margin_data['data']['avlCash']) > margin_required and (margin_required + data["cap_utized"]) < data["capital"]:
            place_new_order = place_order(str(price),"S",stock,quantity,"MIS")
            if isinstance(place_new_order, dict) and "stCode" in place_new_order and place_new_order.get("stCode")== 200:
                orderId = place_new_order['nOrdNo']
                executed = validate.wait_for_order_execution(stock,orderId, max_attempts=3)
                if executed is True:
                    data["cap_utized"] =  data["cap_utized"] + margin_required
                    print("buy PE,Going Down")
                    return True
                if executed is False:
                    cancellation = validate.cancel_and_check_order(orderId)
                    if cancellation is True:
                        return False
                    else:
                        cancellation = validate.cancel_and_check_order(orderId)
                        if cancellation is True:
                            return False
            else:
                return False


def sell_ce():
    if data["debug"] == True:
        return True
    place_new_order = place_order(str(price),"S",stock,quantity,"MIS")
    if isinstance(place_new_order, dict) and "stCode" in place_new_order and place_new_order.get("stCode")== 200:
        orderId = place_new_order['nOrdNo']
        executed = validate.wait_for_order_execution(stock,orderId, max_attempts=3)
        if executed is True:
            margin_required = (float(price) * float(quantity))/5
            print("sell CE,Going Down")
            data["cap_utized"] =  data["cap_utized"] - margin_required
            return True
        if executed is False:
            cancellation = validate.cancel_and_check_order(orderId)
            if cancellation is True:
                return False
            else:
                cancellation = validate.cancel_and_check_order(orderId)
                if cancellation is True:
                    return False
    else:
        return False


def sell_pe():
    if data["debug"] == True:
        return True
    place_new_order = place_order(str(price),"B",stock,quantity,"MIS")
    if isinstance(place_new_order, dict) and "stCode" in place_new_order and place_new_order.get("stCode")== 200:
        orderId = place_new_order['nOrdNo']
        executed = validate.wait_for_order_execution(stock,orderId, max_attempts=3)
        if executed is True:
            # margin_data = client.margin_required(exchange_segment="nse_cm", price=str(price), order_type="L", product="MIS", quantity=quantity, instrument_token=symbol["instrument_token"], transaction_type="S")
            # margin_required = float(margin_data['data']['ordMrgn'])
            margin_required = (float(price) * float(quantity))/5
            print("sell PE,Going up")
            data["cap_utized"] =  data["cap_utized"] - margin_required
            return True
        if executed is False:
            cancellation = validate.cancel_and_check_order(orderId)
            if cancellation is True:
                return False
            else:
                cancellation = validate.cancel_and_check_order(orderId)
                if cancellation is True:
                    return False
    else:
        return False

def execute_trade(trade):
    # Get the current time
    current_time = datetime.now().time()
    # Set the cutoff time to 2:30 PM
    cutoff_time = datetime.strptime("14:30", "%H:%M").time()

    if current_time >= cutoff_time:
        print("Trade not allowed after 2:30 PM")
        return None
    if trade == "buy":
        if symbol["position"] is None and symbol["totrade"] == True:
            if level["trade"]["sl_no"] < 2:
                # Fresh buy
                if buy_ce(symbol["instrument_token"]) == True:
                    symbol["backup_sl"] = level["low"]
                    symbol["traded_level"] = level["level"]
                    symbol["position"] = "buy"
                    level["trade"]["buy"] = True
            else:
                symbol["totrade"] = False

    elif trade == "sell":
        if symbol["position"] is None and symbol["totrade"] == True:
            if level["trade"]["sl_no"] < 2:
                # Fresh sell
                if buy_pe(symbol["instrument_token"]) == True:
                    symbol["position"] = "sell"
                    symbol["backup_sl"] = level["high"]
                    symbol["traded_level"] = level["level"]
                    level["trade"]["sell"] = True

            else:
                symbol["totrade"] = False
    # elif trade == "buy_again":
    #     if symbol["position"] == "buy" and symbol["totrade"] == True:
    #         level["trade"]["sl_no"] += 1

    # elif trade == _again":
    #     elif symbol["position"] == "sell" and symbol["totrade"] == True:
    #         level["trade"]["sl_no"] += 1


def execute_stoploss(stop):
    if stop == "stoploss" and (data["volatile_sl"] != True or level["trade"]["sl_no"] == 0):
        if symbol["position"] == "buy":
            # stop loss hit 
            if sell_ce() == True:
                symbol["position"] = None
                level["trade"]["buy"] = None
                level["trade"]["sl_no"] += 1
                if level["trade"]["sl_no"] == 2:
                    symbol["totrade"] = False

        elif symbol["position"] == "sell":
            # stop loss hit 
            if sell_pe() == True:
                symbol["position"] = None
                level["trade"]["sell"] = None
                level["trade"]["sl_no"] += 1
                if level["trade"]["sl_no"] == 2:
                    symbol["totrade"] = False

    elif symbol.get('volatile') == True:

        if symbol["position"] == "buy":
            #square at breakeven price
            if price >= level["high"]:
                if sell_ce() == True:
                    symbol["position"] = None
                    level["trade"]["sell"] = None
                    level["trade"]["sl_no"] += 1
                    if level["trade"]["sl_no"] == 2:
                        symbol["totrade"] = False

            elif price < (astro_level[symbol["volatile_sl_index"] - 2]):
                if sell_ce() == True:
                    symbol["position"] = None
                    level["trade"]["sell"] = None
                    level["trade"]["sl_no"] += 1
                    if level["trade"]["sl_no"] == 2:
                        symbol["totrade"] = False


        elif symbol["position"] == "sell":
            print(astro_level[symbol["volatile_sl_index"] + 2])
            #square at breakeven price
            if price <= level["low"]:
                if sell_pe() == True:
                    symbol["position"] = None
                    level["trade"]["sell"] = None
                    level["trade"]["sl_no"] += 1
                    if level["trade"]["sl_no"] == 2:
                        symbol["totrade"] = False

            elif price > (astro_level[symbol["volatile_sl_index"] + 2]):
                if sell_pe() == True:
                    symbol["position"] = None
                    level["trade"]["sell"] = None
                    level["trade"]["sl_no"] += 1
                    if level["trade"]["sl_no"] == 2:
                        symbol["totrade"] = False

    if stop == "trailing_stoploss":
        if symbol["position"] == "buy":
            # stop loss hit 
            if sell_ce() == True:
                symbol["position"] = None
                level["trade"]["buy"] = None
                level["trade"]["sl_no"] += 1
                if level["trade"]["sl_no"] == 2:
                    symbol["totrade"] = False
                reset.clear_data_on_sl(stock,symbol["detected_level"])

        elif symbol["position"] == "sell":
            # stop loss hit 
            if sell_pe() == True:
                symbol["position"] = None
                level["trade"]["sell"] = None
                level["trade"]["sl_no"] += 1
                if level["trade"]["sl_no"] == 2:
                    symbol["totrade"] = False
                reset.clear_data_on_sl(stock,symbol["detected_level"])


def hit_target(hit):
    if hit == "target_achived":
        if symbol["position"] == "buy":
            # stop loss hit 
            if sell_ce() == True:
                symbol["position"] = None
                level["trade"]["buy"] = None
                reset.clear_data_on_tl(stock)
        elif symbol["position"] == "sell":
            # stop loss hit 
            if sell_pe() == True:
                symbol["position"] = None
                level["trade"]["sell"] = None
                reset.clear_data_on_tl(stock)

    if symbol.get('volatile') == True:

        if symbol["position"] == "buy":
            if price < (astro_level[symbol["volatile_sl_index"] - 2]):
                if sell_ce() == True:
                    symbol["position"] = None
                    level["trade"]["sell"] = None
                    level["trade"]["sl_no"] += 2
                    symbol["totrade"] = False

        elif symbol["position"] == "sell":
            #square at breakeven price
            if price > (astro_level[symbol["volatile_sl_index"] + 2]):
                if sell_pe() == True:
                    symbol["position"] = None
                    level["trade"]["sell"] = None
                    level["trade"]["sl_no"] += 2
                    # if level["trade"]["sl_no"] == 2:
                    symbol["totrade"] = False


    if symbol["position"] == "buy":
        if price < symbol["backup_sl"] and symbol["detected_level"] != symbol["traded_level"] and symbol.get("volatile") != True:
            if sell_ce() == True:
                symbol["position"] = None
                level["trade"]["sell"] = None
                level["trade"]["sl_no"] += 2
                symbol["totrade"] = False
    
    if symbol["position"] == "sell":
        if price > symbol["backup_sl"] and symbol["detected_level"] != symbol["traded_level"] and symbol.get("volatile") != True:
            if sell_pe() == True:
                symbol["position"] = None
                level["trade"]["sell"] = None
                level["trade"]["sl_no"] += 2
                # if level["trade"]["sl_no"] == 2:
                symbol["totrade"] = False
            
def login_today():     
    global client,QUANTITY
    consumer_key="<Your_consumer_key>"   #This will be generate while registring for the kotak neo API
    consumer_secret="<Your_consumer_secret>"  #This will be generate while registring for the kotak neo API

    def on_message(message):
        global price,client
        try:
            price = message[0]["ltp"]
        except Exception as e:
            print(f"error {e}")
    
    def on_error(error_message):
        print(error_message)
    # QUANTITY = input("Enter Quantity : ")
    client = NeoAPI(consumer_key=consumer_key,consumer_secret=consumer_secret,environment="prod",on_message=on_message, on_error=on_error)  
    client.login(mobilenumber="+91<Your_contact_no>", password="<Your_password>")
    # login_token = input("Input todays token:")
    client.session_2fa(OTP="<MPIN_Kotak_neo>")



from_config = configuration.GetConfig()
init_astro_parser = from_config.get_astro_data()
astro_level = astro_parser.astro_level
data = from_config.get_stock_hub()
ce_data = from_config.get_ce_data()
pe_data = from_config.get_pe_data()
for symbol in data["symbols"]:
    if symbol["position"] == None:
        symbol["totrade"] = None

if data["debug"] == False:
    login_today()
    validate = validation.ValidataTrade(client) 
instrument_tokens = [{'instrument_token': '22', 'exchange_segment': 'nse_cm'}, {'instrument_token': '25', 'exchange_segment': 'nse_cm'}, {'instrument_token': '14672', 'exchange_segment': 'nse_cm'}, {'instrument_token': '236', 'exchange_segment': 'nse_cm'}, {'instrument_token': '335', 'exchange_segment': 'nse_cm'}, {'instrument_token': '15141', 'exchange_segment': 'nse_cm'}, {'instrument_token': '8479', 'exchange_segment': 'nse_cm'}, {'instrument_token': '17875', 'exchange_segment': 'nse_cm'}, {'instrument_token': '17963', 'exchange_segment': 'nse_cm'}, {'instrument_token': '19943', 'exchange_segment': 'nse_cm'}, {'instrument_token': '1232', 'exchange_segment': 'nse_cm'}, {'instrument_token': '1394', 'exchange_segment': 'nse_cm'}, {'instrument_token': '2031', 'exchange_segment': 'nse_cm'}, {'instrument_token': '2664', 'exchange_segment': 'nse_cm'}, {'instrument_token': '2885', 'exchange_segment': 'nse_cm'}, {'instrument_token': '3273', 'exchange_segment': 'nse_cm'}, {'instrument_token': '3506', 'exchange_segment': 'nse_cm'}, {'instrument_token': '3518', 'exchange_segment': 'nse_cm'}, {'instrument_token': '10726', 'exchange_segment': 'nse_cm'}, {'instrument_token': '4306', 'exchange_segment': 'nse_cm'}, {'instrument_token': '4503', 'exchange_segment': 'nse_cm'}, {'instrument_token': '11654', 'exchange_segment': 'nse_cm'}]
while 1:
    current_time = datetime.now().time()
    # Set the cutoff time to 2:30 PM
    cutoff_time = datetime.strptime("09:14", "%H:%M").time()

    if current_time >= cutoff_time:
        data = from_config.get_stock_hub()
        try:
            try:
                ltp_response = client.quotes(instrument_tokens= instrument_tokens, quote_type = "ltp")
                # data = [{item['trading_symbol']: item['instrument_token']} for item in ltp_response['message']]

                prices = [{item['trading_symbol']: float(item['ltp'])} for item in ltp_response['message']]
            except:
                pass
            data = from_config.get_stock_hub()
            go_up = touchup.touchandgo_Up(data)
            go_down = touchdown.touchandgo_Down(data)
            reset = reset_data.SymbolDataManager(data)

            if data["debug"] == True:
                rel = int(input("Reliance:"))
                hdfc = int(input("HDFC:"))
                prices = [{"RELIANCE-EQ": rel}, {"HINDUNILVR-EQ": hdfc}]
            # Detect price levels and update JSON data
            
            level_detector.detect_price_levels(prices, astro_level, data)

            #Prepair the shapes
            for stock_price in prices:
                for stock, price in stock_price.items():
                    go_up.make_shape_buy(stock, price)
                    go_up.reverse_buy(stock, price, "GREEN")
                    go_down.make_shape_sell(stock, price)
                    go_down.reverse_sell(stock, price, "GREEN")
                    #Analyse the volumes for the shaped formed
                    for symbol in data["symbols"]:
                        if symbol["key"] == stock:
                            if symbol["totrade"] == None:
                                print("Analysisng the stocks .....")
                                # if astrocrosses.analyze_stock(symbol["key"],astro_level,4) is True:
                                symbol["totrade"] = True

                            for level in symbol["shapes"]:
                                pos = position.TradePosition(price,symbol,level,astro_level,data)
                                if symbol["detected_level"] == level["level"]:
                                    if level["status"] == "completed" and level["volume"] is None:

                                        analyser = sounds.VolumeAnalyser(data)
                                        # Provide start and end times in YYYY-MM-DD HH:MM:SS format
                                        start_time = level["shapetime"]
                                        end_time = level["endshapetime"]

                                        # Analyze volume for the given time period
                                        sounding = analyser.analyze_volume(symbol["key_yf"], start_time, end_time)

                                        if level["volume"] is None:
                                            if sounding is True:
                                                level["volume"] = True
                                            elif sounding is False:
                                                level["volume"] = False
                                    
                                    if level["volume"] is True:
                                        trade = pos.take_trades()
                                        execute_trade(trade)
                                        stops = pos.stopout()
                                        if stops == "stoploss" and data["volatile_sl"] == True and  level["trade"]["sl_no"] > 0:
                                            symbol["volatile"] = True
                                            symbol["volatile_sl_index"] = astro_level.index(level["level"])
                                        execute_stoploss(stops)
                                        pos.target(trade)
                            
                                target = pos.get_target("GREEN")
                                hit_target(target)
                                            # execute_trade(trade)

                                            
            # Save the updated data back to the JSON file
            from_config.write_data_json(data)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
            email_alert.send_email("Bug Alert!", error_message)
            break  # Exit the loop or handle the error appropriately




