import os
import sys
from lib import filehandler
from lib import astro_parser

# HOME = os.environ.get('JIRA_HOME_DIR') # After setting Env. variable restart the computer
HOME = rf"D:/Algo/version2/runner/sanpro/"
STOCKHUB = rf"{HOME}logger/stock_hub.json"
ASTROSHEET = rf"{HOME}input/data_asto.xlsx"
CEOPTION = rf"{HOME}input/ce_options.json"
PEOPTION = rf"{HOME}input/pe_options.json"
PRICELEVEL = 2800


class GetConfig:
    '''Get Configuration from JSON file and service tokens from txt file/docker secrets.'''

    def __init__(self):
        self.file_operation = filehandler.Persistency()

        # Configurations
        self.__stock_data = self.file_operation.read_json(STOCKHUB)
        self.__call_data = self.file_operation.read_json(CEOPTION)
        self.__put_data = self.file_operation.read_json(PEOPTION)


    # Getter methods
    def get_stock_hub(self):
        ''' Get last sync time 
        Returns:
            dic: A dictionary containing stocks status data
        '''
        return self.__stock_data

    def get_ce_data(self):
        ''' Get ce data
        Returns:
            dic: A string representing the ce data
        '''
        return self.__call_data

    def get_pe_data(self):
        '''get pe data.
        Returns:
            str: A string representing the pe data
        '''
        return self.__put_data
    
    def get_astro_data(self):
        '''get pe data.
        Returns:
            str: A string representing the pe data
        '''
        self.__astro_data  = astro_parser.xl_parse(PRICELEVEL,ASTROSHEET)
        return  self.__astro_data
    def write_data_json(self,data):
        '''write data inside json.
        Returns:
            status : True/False
        '''
        self.file_operation.save_state(STOCKHUB,data)         


    