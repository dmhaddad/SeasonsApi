
"""
Public Holiday API covers holidays in the United States for the year 2025.

"""


import requests
from pprint import pprint
import json

HOLIDAY_API_URL = "https://date.nager.at/api/v3/PublicHolidays"

# User inputs a date in MMDDYYYY format in Seasons-API.py. Will need to convert this to YYYY-MM-DD format for the holiday API.

def holiday(date:str):

    # Convert MMDDYYYY to YYYY-MM-DD
    month = date[0:2]
    day = date[2:4]
    year = date[4:]
    formatted_date = f"{year}-{month}-{day}" 

    # Get all holidays for the year 2025 in the US
    response = requests.get(f"{HOLIDAY_API_URL}/2025/US") 

    # Check if the request was successful
    if response.status_code != 200:
        print("Error fetching holiday data")
        return None
    
    holidays = response.json()

    # Look for a matching holiday
    for holiday in holidays:
        if holiday.get("date") == formatted_date:
            return holiday.get("localName")
    return None