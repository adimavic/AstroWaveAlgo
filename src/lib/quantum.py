import logging

# Configure the logging settings
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

risk_factor = 0.50
base_quantity = 250
max_loss = 1200
max_loss_single_lot = 3000

class Risk_Manager():
    def __init__(self,client):
        self.client = client
        pass

    def get_account_fund_order_margin(self,instrument_token, price): # get the max passoible quanityt for the trade
        try:
            margin_data = self.client.margin_required(exchange_segment="nse_fo", price=price, order_type="L", product="NRML", quantity="250", instrument_token=instrument_token, transaction_type="B")
            avlCash = float(margin_data['data']['avlCash'])
            margin_required = float(margin_data['data']['ordMrgn'])
            max_possible_quantity = int(round(avlCash / margin_required)) * base_quantity
            return max_possible_quantity
        except Exception as e:
            # Log the error if it occurs
            logging.error(f'Error in get_account_fund_order_margin: {e}')
            max_possible_quantity=750
            return max_possible_quantity

    def calculate_option_quantity(self, h, low, max_possible_quantity):
        try:
            if max_possible_quantity is not None:
                risk = (h - low) * risk_factor
                calculated_risk = risk * base_quantity

                if calculated_risk < max_loss:
                    calculated_quantity = int(max_loss // calculated_risk * base_quantity)

                    # Check if calculated_quantity can be afforded, otherwise adjust to the closest multiple of 250
                    measured_quantity = int(round(calculated_quantity / base_quantity)) * base_quantity
                    final_quantity = min(measured_quantity, max_possible_quantity)

                elif calculated_risk < max_loss_single_lot:
                    final_quantity = base_quantity
                else:
                    final_quantity = 0
                if final_quantity >= 0 :
                    return final_quantity
                else:
                    logging.error(f'Error quality is negative or empty')
                    return None
                
        except Exception as e:
            # Log the error if it occurs
            logging.error(f'Error in calculate_option_quantity: {e}')
            return None

# Instantiate Risk_Manager
# risk_manager = Risk_Manager()

# # Example usage:
# h_value = 9
# low_value = 10
# max_possible_quantity = 500
# result_quantity = risk_manager.calculate_option_quantity(h_value, low_value, max_possible_quantity)

# print("Final Quantity:", result_quantity)
