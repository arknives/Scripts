from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Get the list of license numbers from the user
license_numbers = input("Please enter the list of license numbers, separated by commas: ").split(",")

# Initialize the webdriver
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("https://search.dca.ca.gov/")

# Select option 30 from the dropdown menu
dropdown = Select(driver.find_element(By.ID, "boardCode"))
dropdown.select_by_value("30")

# Select option 114 from the dropdown menu
dropdown = Select(driver.find_element(By.ID, "licenseType"))
dropdown.select_by_value("114")

# Loop over the license numbers and search for each one
for license_number in license_numbers:
    # Enter the license number
    license_number_field = driver.find_element(By.ID, "licenseNumber")
    license_number_field.clear()  # Clear the field in case there was a previous value
    license_number_field.send_keys(license_number)

    # Click the search button
    search_button = driver.find_element(By.ID, "srchSubmitHome")
    search_button.click()

    # Wait for the search results to load
    driver.implicitly_wait(5)

    # Get the full name and license status
    try:
        full_name = driver.find_element(By.XPATH, '//*[@id="0"]/footer/ul[1]/li[1]/h3')
        license_status = driver.find_element(By.XPATH, '//*[@id="0"]/footer/ul[1]/li[4]')
        print(f"{full_name.text} - {license_status.text}")
    except:
        print(f"License {license_number} not found")

# Keep the browser open
input("Press enter to close the browser...")
driver.quit()
