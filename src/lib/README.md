# lib Folder  

This folder contains all the essential libraries and scripts required to run `main.py` and the algo effectively. Each script serves a specific purpose to ensure smooth and accurate execution of the algorithm. Below is a breakdown of the scripts and their functionalities:  

---

### Scripts  

1. **`astro_parser.py`**  
   - **Purpose**: Parses the `astro.xls` file and converts its data into the desired format required for processing astro levels in the algo.  

2. **`change_strike.py`**  
   - **Purpose**: Adjusts the strike price to the ATM (At-the-Money) option for both call (CE) and put (PE) options.  
   - **Input**: Uses `pe_options.json` and `ce_options.json` files for parsing option data.  

3. **`email_alert.py`**  
   - **Purpose**: Sends email notifications when the code encounters errors while running.  
   - **Details**:  
     - The algo runs at high speed in the cloud, making it challenging to monitor in real-time.  
     - This script ensures you are alerted immediately so you can manually intervene if necessary.  

4. **`file_handler.py`**  
   - **Purpose**: Manages file operations such as reading and writing data.  
   - **Details**: Essential for handling the multiple files used by the algo.  

5. **`level_detector.py`**  
   - **Purpose**: Detects stock prices in relation to astro levels.  
   - **Details**: Astro levels are used as benchmarks for drawing W and M patterns, which are critical for trading logic.  

6. **`quantum.py`**  
   - **Purpose**: Adjusts the trade quantities dynamically based on predefined logic.  

7. **`reset_data.py`**  
   - **Purpose**: Resets data in the `stock_hub.json` file according to the algo's logic.  

8. **`sma_crossover.py`**  
   - **Purpose**: Calculates Simple Moving Averages (SMA) for stocks and identifies SMA crossovers (e.g., 5-SMA and 200-SMA).  

9. **`sma_tv.py`**  
   - **Purpose**: Fetches live SMA data directly from TradingView.  

10. **`sounds.py`**  
    - **Purpose**: Analyzes the volume of M and W patterns.  
    - **Details**: Determines whether the volume confirms the trading signals.  

11. **`touchdown.py` and `touchup.py`**  
    - **Purpose**: Creates the shapes for M and W patterns, which are integral to the algo's trading strategy.  

12. **`validate.py`**  
    - **Purpose**: Ensures buy or sell orders are executed within 3 seconds on the exchange.  
    - **Details**:  
      - If an order is not executed within the time frame, the script cancels the current order and places a new one with a higher probability of being filled.  

---

### Summary  

The **`lib`** folder is the backbone of the algo, containing specialized scripts for every major function, including:  
- Parsing astro levels.  
- Adjusting strike prices.  
- Detecting SMA crossovers.  
- Validating and executing trades.  
- Managing files and resetting data.  
- Sending alerts for seamless monitoring.  

This modular design ensures that the algo runs efficiently, remains adaptable to market conditions, and handles errors gracefully.  