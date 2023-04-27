import csv
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import openpyxl

# 1. You must drag and drop the CSV file onto this py file.
# 2. This script will open a browser in chrome and search for the licenses.
# 3. The output will be a xlsx file created in the same location as the py file.

# Get the path of the script
script_path = Path(sys.argv[0]).resolve().parent

# Get the list of license numbers from the user
if len(sys.argv) < 2:
    print("Please drag and drop the CSV file onto the script.")
    sys.exit()

csv_file_path = sys.argv[1]
license_numbers = []

with open(csv_file_path, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if row:  # check if the row is not empty
            # Split the row into individual items using the delimiter
            items = row[0].split(',')
            for item in items:
                # Append each item to the license_numbers list
                license_numbers.append(item)

# Initialize the webdriver
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("https://search.dca.ca.gov/")

# Create a new workbook
workbook = openpyxl.Workbook()
sheet = workbook.active

# Add header row to the sheet
sheet.append(["License Number", "Full Name", "License Status", "Expiration Date"])

# Loop over the license numbers and search for each one
for license_number in license_numbers:
    # Select option 30 from the dropdown menu
    dropdown = Select(driver.find_element(By.ID, "boardCode"))
    dropdown.select_by_value("30")

    # Select option 114 from the dropdown menu
    dropdown = Select(driver.find_element(By.ID, "licenseType"))
    dropdown.select_by_value("115")
    
    # Enter the license number
    license_number_field = driver.find_element(By.ID, "licenseNumber")
    # Clear the field in case there was a previous value
    license_number_field.clear()
    license_number_field.send_keys(license_number)

    # Click the search button
    search_button = driver.find_element(By.ID, "srchSubmitHome")
    search_button.click()

    # Wait for the search results to load
    driver.implicitly_wait(5)

    # Get the full name and license status
    full_name = None
    try:
        full_name = driver.find_element(By.XPATH, '//*[@id="0"]/footer/ul[1]/li[1]/h3')
        license_status = driver.find_element(By.XPATH, '//*[@id="0"]/footer/ul[1]/li[4]')
        expiration_date = driver.find_element(By.XPATH, '//*[@id="0"]/footer/ul[1]/li[5]')
        print("{:<15} {:<30} {:<25} {:<15}".format(license_number, full_name.text, license_status.text, expiration_date.text))

        # Add license info to the sheet
        sheet.append([license_number, full_name.text, license_status.text, expiration_date.text])
    except:
        print(f"{full_name.text} - License {license_number} not found")

    # Go back to the search page for the next license number
    driver.back()

# Save the workbook in the same location as the script
excel_file_path = script_path / "license_info.xlsx"
workbook.save(excel_file_path)
print(f"\nLicense info saved to {excel_file_path}")

# Closing the Script
driver.quit()
