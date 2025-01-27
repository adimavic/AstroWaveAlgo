"""
Copyright (c) 2023 by Realthingks GmbH                            All rights reserved.

This software is copyright protected and proprietary to Realthingks GmbH.
Realthingks GmbH grants to you only those rights as set out in the license conditions.
All other rights remain with Realthingks GmbH.
"""

"""
This script is used to read and write files.
"""
import json
from datetime import datetime

class Persistency:
    """Class for handling persistence operations."""

    def __init__(self):
        """Initialize the Persistency instance."""
        pass

    def read_json(self, config_file):
        """Read data from the specified JSON file.

            Args:
                config_file (str): The file path of the JSON configuration file.

            Returns:
                dict: A dictionary representing the configuration read from the JSON file.

            Raises:
                FileNotFoundError: If the specified file is not found.
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as config:
                configuration = json.load(config)
            return configuration
        except FileNotFoundError:
            print(f"File not found: {config_file}")
            return {}

    def write_json(self, data, config_file):
        """Write data into the specified JSON file.

        Args:
            data (dict): The data to be written into the JSON file.
            config_file (str): The file path of the JSON configuration file.

        Returns:
            bool: True if the write operation is successful, False otherwise.
        """
        try:
            with open(config_file, 'w', encoding='utf-8') as config_file:
                json.dump(data, config_file, indent=2)
            return True
        except Exception as e:
            print(f"Error writing to file {config_file}: {e}")
            return False

    def read_text_file(self, config_file):
        """Read data from the specified text file.

        Args:
            config_file (str): The file path of the text file.

        Returns:
            str: The content of the text file.

        Raises:
            FileNotFoundError: If the specified file is not found.
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as config:
                configuration = config.read().strip()
            return configuration
        except FileNotFoundError:
            print(f"File not found: {config_file}")
            return None

    def write_text_file(self, data, config_file):
        """Write text data into the specified text file.

        Args:
            data (str): The text data to be written into the file.
            config_file (str): The file path of the text file.

        Returns:
            bool: True if the write operation is successful, False otherwise.
        """
        try:
            with open(config_file, 'w', encoding='utf-8') as text_file:
                text_file.write(data)
            return True
        except Exception as e:
            print(f"Error writing to text file {config_file}: {e}")
            return False
    def save_state(self,file_name, data):
        with open(file_name, 'w') as file:
            json.dump(self.convert_datetime_to_str(data), file, indent=4)

    # Helper function to convert datetime objects to strings
    def convert_datetime_to_str(self,obj):
        if isinstance(obj, dict):
            return {k: self.convert_datetime_to_str(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_datetime_to_str(i) for i in obj]
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return obj