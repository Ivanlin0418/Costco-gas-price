import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

URL = "https://www.costco.com/warehouse-locations"


#GLOBAL VARIABLES
FIND_BUTTON = "button.btn.btn-primary[automation-id='findButton']"
TABLE_ROW = "tr.warehouse.table-row"
ADDRESS_LINE1 = "span[automation-id^='warehouseAddressLine1Output']"
WAREHOUSE_NAME = "a.warehouse-name"
PHONE_NUMBER = "span.hidden-xs.hidden-sm"
REGULAR_GAS_PRICE = "span[automation-id='regularGasPrice']"
PREMIUM_GAS_PRICE = "span[automation-id='premiumGasPrice']"

def findNearestCostcoGasCenter(zipCode):
    """
    This function takes a zip code as input and finds the nearest Costco gas center using Selenium to automate the web browser.
    Steps:
    1. Initializes the Chrome WebDriver with verbose logging.
    2. Navigates to the Costco warehouse locations page.
    3. Enters the provided zip code into the search input field and clicks the find button.
    4. Waits for the warehouse row to be present and clicks on it.
    5. Extracts and prints the location details including the warehouse name, address, city, state, zip code, and phone number.
    6. Attempts to extract and print the regular and premium gas prices if available.
    7. Handles exceptions if gas prices are not available or if any other error occurs during the extraction process.
    
    Args:
    zipCode (str): The zip code to search for the nearest Costco gas center.
    
    Returns:
    int: Returns 0 upon successful completion.    
    """
    
    options = webdriver.ChromeOptions()
    options.add_argument('--verbose')
    driver = webdriver.Chrome(options=options)  

    driver.get(URL)

    try:
        search_input = driver.find_element(By.ID, "search-warehouse")
        search_input.clear()
        search_input.send_keys(zipCode)

        find_button = driver.find_element(By.CSS_SELECTOR, FIND_BUTTON)
        find_button.click()

        # Wait for the warehouse row to be present
        warehouse_row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, TABLE_ROW))
        )
        warehouse_row.click()

        # Extracting location details
        warehouse_row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, TABLE_ROW))
        )
        location_name = warehouse_row.find_element(By.CSS_SELECTOR, WAREHOUSE_NAME).text
        address_line1 = warehouse_row.find_element(By.CSS_SELECTOR, ADDRESS_LINE1).text
        city_state_zip = warehouse_row.find_elements(By.CSS_SELECTOR, "span")[1].text
        phone_number = warehouse_row.find_element(By.CSS_SELECTOR, PHONE_NUMBER).text

        print(f"Location Name: {location_name}")
        print(f"Address: {address_line1}, {city_state_zip}")
        print(f"Phone Number: {phone_number}")


        try:
            regular_price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, REGULAR_GAS_PRICE))
            ).text
            premium_price = driver.find_element(By.CSS_SELECTOR, PREMIUM_GAS_PRICE).text
            print("Gas prices extracted.")
            print(f"Regular Gas Price: {regular_price}")
            print(f"Premium Gas Price: {premium_price}")
        except TimeoutException:
            print("No gas prices available.")
        except Exception as e:
            print(f"An error occurred while retrieving gas prices: {e}")
        return 0 
    
    except TimeoutException:
        print("Timeout while waiting for elements.")
    except StaleElementReferenceException:
        print("Stale element reference exception occurred.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()  
    return -1  # Error code if any exception occurs

def main():
    parser = argparse.ArgumentParser(description='Find the nearest Costco gas center.')
    parser.add_argument('zipCode', type=int, help='Zip code to search for nearest Costco gas center')
    args = parser.parse_args()
    findNearestCostcoGasCenter(args.zipCode)

if __name__ == "__main__":
    main()
