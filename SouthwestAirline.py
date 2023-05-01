import time
import gspread
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from oauth2client.service_account import ServiceAccountCredentials
import urllib.parse

# Define the URL of the Google Sheet
sheet_url = 'https://docs.google.com/spreadsheets/d/1-NsnlfcXB21EN77Zq7UfD4rF89PTKJg7WDASu6V2g00/edit#gid=979659718'

# Define the Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Joe\Downloads\vast-pride-385101-f6a304aed2e4.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open_by_url(sheet_url).sheet1

# Get all the rows from the Google Sheet
rows = sheet.get_all_records()

# Define the column index to write to
column_index = 16  # index 4 corresponds to column D

# Define the input and output date formats
input_format = '%A, %B %d, %Y'
output_format = '%Y-%m-%d'

# Start the Chrome driver
driver = webdriver.Chrome()

# Loop through all the rows of the Google Sheet
for row in rows:
    # Get the values from the current row
    travel_date = row['Travel Date']
    departure = row['From (airport)']
    arrival = row['To (airport)']
    departure_time = row['Departure time (local time)']
    arrival_time = row['Arrival time (local time)']
    cash_or_points = row['Cash or Points']
    points_cost = row['Point Cost']
    out_of_pocket_cash_cost = row['Out of Pocket Cash Cost']

    # Convert the input date string to a datetime object
    date_obj = datetime.strptime(travel_date, input_format)

    # Check if travel_date has not passed today's date
    if date_obj.date() < datetime.now().date():
        print(f"Skipping travel date {travel_date} as it has passed today's date")
        continue

    # Convert the datetime object to the output date format
    output_str = date_obj.strftime(output_format)

    # Convert Cash or Points
    if cash_or_points == 'Cash':
        cash_or_pounts = 'USD'
    elif cash_or_points == 'Points':
        cash_or_pounts = 'POINTS'
        
    # Build the URL using urllib.parse.urlencode()
    params = {
        'int': 'HOMEQBOMAIR',
        'adultPassengersCount': '1',
        'departureDate': output_str,
        'destinationAirportCode': arrival,
        'fareType': cash_or_points,
        'originationAirportCode': departure,
        'passengerType': 'ADULT',
        'promoCode': '',
        'returnDate': '',
        'tripType': 'oneway',
        'from': '',
        'to': '',
        'adultsCount': '1',
        'departureTimeOfDay': 'ALL_DAY',
        'reset': 'true',
        'returnTimeOfDay': 'ALL_DAY'
    }

    url = "https://www.southwest.com/air/booking/select.html?" + urllib.parse.urlencode(params)

    # Print the url
    print(url)
    sheet.update_cell(rows.index(row) + 2, 16, url)
    
input("Press enter to close")
