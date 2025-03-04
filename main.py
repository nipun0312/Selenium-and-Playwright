from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Replace with your credentials
USERNAME = "nipun@gmail.com"
PASSWORD = "asdf1234"

# Path to your WebDriver (Update this to your actual path)
CHROME_DRIVER_PATH = "chromedriver.exe"

# Initialize WebDriver Service
service = Service(CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Start WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open Facebook Login Page
    driver.get("https://www.facebook.com/")

    # Wait for page to load
    time.sleep(2)

    # Find username field and input email/phone
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(USERNAME)

    # Find password field and input password
    password_input = driver.find_element(By.ID, "pass")
    password_input.send_keys(PASSWORD)

    # Press Enter to login
    password_input.send_keys(Keys.RETURN)

    # Wait for login to process
    time.sleep(5)

    print("Login successful!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
