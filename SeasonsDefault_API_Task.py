"""
Task: Ask the User for a date, based on the date, tell them what Season we are in (meteorological seasons) in English, Spanish, or both based on their input.
Meteorological Seasons:


Description: This program stores the start of each season as variables which is used to determine the actual season based on the month extracted from the date inputted by the user.
The user in prompted to enter basic identifying information (full name, email, phone number) which is validated using the NameAPI Risk Detector API to reduce fraudulent users. If the 
user is likely vaid, they are then prompted to enter a date in MMDDYYYY format and their language preference (English, Spanish, or both). The program then outputs the corresponding season(s).
If the date corresponds to a US holiday in 2025, the holiday name is also displayed in the selected language(s) using the Public Holiday API and a predefined translation table/function.

Author: David Haddad

"""

from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from pprint import pprint
import json
from holidayApi import holiday
from holiday_translations import holiday_translation_spanish

load_dotenv()

# Meteorological seasons (starting months)
spring_start = 3 
summer_start = 6 
fall_start = 9 
winter_start = 12

# NameAPI Risk Detector API setup
RISK_DETECTOR_URL="https://api.nameapi.org/rest/v5.3/riskdetector/person" 
risk_detector_api_key = os.getenv("NAME_API_KEY")


def get_person_info():
    while True:
        name = input("Enter your full name: ").strip()
        email = input("Enter your email address: ").strip()
        if "@" not in email or "." not in email: # Basic email format validation
            print("\nPlease enter a valid-looking email address (must contain '@' and '.').\n")
            continue
        phone = input("Enter your phone number, starting with the country code (digits only): ").strip()
        if not email or not phone:
            print("\nEmail and phone are required. Please enter a value for both fields.\n")

        else:
            return name, email, phone

def get_date(): 
    while True: 
        user_date = input('Which season am I? Please enter a date in MMDDYYYY format: ')
        try: 
            datetime.strptime(user_date, "%m%d%Y") 
            return user_date 
        except ValueError: 
            print('Incorrect format. Please try again. \n')

def get_language(): 
    while True: 
        language = input('What is your language of preference? Please enter: "English", "Spanish", or "both".: \n').lower().strip() 
        if language in ["english", "spanish", "both"]: 
            return language 
        else: print('Invalid input. Please try again. \n')

def english_season(month:int): 
    if spring_start <= month < summer_start: 
        return "Spring" 
    elif summer_start <= month < fall_start: 
        return "Summer" 
    elif fall_start <= month < winter_start: 
        return "Fall" 
    else: return "Winter"

def spanish_season(month:int): 
    if spring_start <= month < summer_start: 
        return "La primavera" 
    elif summer_start <= month < fall_start: 
        return "El verano" 
    elif fall_start <= month < winter_start: 
        return "El otoño" 
    else: return "El invierno"

""" 
----------NAME API Docs----------
A score > 0 means there's a risk. Zero is the neutral value; nothing bad detected yet there's nothing good either. 
A negative value means that the record does look genuine.
    [-1,0) : no risks detected, record looks good
    0      : neutral
    (0,1]  : one or more risks detected (risk present)
    if score > 0:
        return False  # likely invalid
"""

# Call NameAPI Risk Detector
def call_risk_detector(name, email, phone):
    params = { "apiKey": risk_detector_api_key, "envelope": "true" }

    payload = { 
        "context": {}, 
        "inputPerson": { 
            "type": "NaturalInputPerson",
        
        "emailAddresses": [ 
            { 
                "type": "EmailAddressImpl", 
                "emailAddress": email,
            }
        ], 
        "correspondenceLanguage": "en", 
        "telNumbers": [ 
            {
                "type": "SimpleTelNumber", 
                "fullNumber": phone,
            }
        ],

        "personName": {
            "nameFields": [
                {"string": name, "fieldType": "FULLNAME"}, 
                #{"string": "YourLast", "fieldType": "SURNAME"},
                ]
            },
        },                
    }

    response = requests.post(
        RISK_DETECTOR_URL,
        params=params, 
        json=payload)
    
    data = response.json()
    return data


def main():
    name, email, phone = get_person_info()

    risk_data = call_risk_detector(name, email, phone)
    print()
    #print("Full Risk Detector response:")
    #pprint(risk_data)

    input_results = json.loads(risk_data['result'])

    risk_score = input_results['score']

    if risk_score > 0:
        worst = input_results.get("worstRisk", {})
        risk_item = worst.get("dataItem", "Unknown item")
        risk_reason = worst.get("reason", "No reason provided")
        risk_type = worst.get("riskType", "No risk type provided")
        if risk_item == "NAME":
            print(f'User is likely invalid due to the "Full name" field input. Please enter a valid full name.')
            print(f'Potential reasons include: {risk_type}, {risk_reason}.')
        elif risk_item == "EMAIL":
            print(f'User is likely invalid due to the "Email address" field input. Please enter a valid email address.')
            print(f'Potential reasons include: {risk_type}, {risk_reason}.')
        elif risk_item == "TEL":
            print(f'User is likely invalid due to the "Phone number" field input. Please enter a valid phone number.') 
            print(f'Potential reasons include: {risk_type}, {risk_reason}.')
        
        return None
    else:
        print("User is likely valid based on the name, phone and email provided. Proceeding to season determination.\n")

    date = get_date() 
    language = get_language()
    month = int(date[:2])
    holiday_name = holiday(date) # Call holiday API to get holiday name in English
    #holiday_name_spanish = holiday_name  # Initialize Spanish holiday name


    print()

    if language == 'english': 
        print(english_season(month)) 
    elif language == 'spanish': 
        print(spanish_season(month)) 
    elif language == 'both': 
        print(f'{english_season(month)} - {spanish_season(month)}')
    
    holiday_name_spanish = holiday_translation_spanish(holiday_name) # Translate holiday name to Spanish
    
    if holiday_name and language == 'english':
        print(f'\nNote: The date you entered corresponds to the holiday: {holiday_name}\n')
    elif holiday_name and language == 'spanish':
        print(f'\nNota: La fecha que ingresaste corresponde al feriado: {holiday_name_spanish}\n')
    elif holiday_name and language == 'both':
        print(f'\nNote/Nota: The date you entered corresponds to the holiday/feriado: {holiday_name} - {holiday_name_spanish}\n')

if __name__ == "__main__":
    main()