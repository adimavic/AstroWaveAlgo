from time import sleep
class ValidataTrade():
    def __init__(self,client):
        self.client = client


    def wait_for_order_execution(self,trdSym, order_id, max_attempts=60):
        # Check the order status until it's filled or a maximum number of attempts is reached
        for _ in range(max_attempts):
            sleep(0.5)  # import time
            order_status = self.client.order_report()
            for data in range(len(order_status["data"])):
                if order_status["data"][data]["nOrdNo"] == order_id:
                    if order_status["data"][data]["ordSt"] == "complete":
                        print(f"Order {trdSym} has been placed.")
                        return True  # Order is filled
                    else:
                        pass
        return False 
    def cancel_and_check_order(self,order_id):
        # Attempt to cancel the order
        cancel_response = self.client.cancel_order(order_id)
        if cancel_response["stCode"] == 200:
            print(f"Order {order_id} has been successfully cancelled.")
            return True
        else:
            print(f"Failed to cancel order {order_id}. Status: {cancel_response.status}")
            return False