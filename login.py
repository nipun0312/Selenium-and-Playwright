from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set the correct path to your ChromeDriver
CHROME_DRIVER_PATH = "chromedriver.exe"

# Facebook credentials (Replace with your own)
USERNAME = "nipun@gmail.com"
PASSWORD = "asdf1234"

# Initialize WebDriver
service = Service(CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)

try:
    # Open Facebook Login Page
    driver.get("https://www.facebook.com/")

    # Wait for page to load
    time.sleep(2)

    # Locate the username field using XPath and input email/phone
    email_input = driver.find_element(By.XPATH, "//input[@name='email']")
    email_input.send_keys(USERNAME)

    # Locate the password field using XPath and input password
    password_input = driver.find_element(By.XPATH, "//input[@name='pass']")
    password_input.send_keys(PASSWORD)

    # Locate the login button using XPath and click it
    login_button = driver.find_element(By.XPATH, "//button[@name='login']")
    login_button.click()

    # Wait for login to process
    time.sleep(5)

    print("Login successful!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
