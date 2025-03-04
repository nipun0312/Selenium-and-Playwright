from playwright.sync_api import sync_playwright, Playwright
from rich import print
import time  # Optional delay for better visualization


def run(playwright: Playwright):
    start_url = "https://www.daraz.com.bd/catalog/?q=router"
    chrome = playwright.chromium
    browser = chrome.launch(headless=False)  # Open browser

    # Step 1: Open search results page ONCE
    page = browser.new_page()
    page.goto(start_url)
    print("Opened search results page.")

    # Step 2: Collect all product links
    links = page.locator("a[href*='tp-link']").all()  # Get all TP-Link product links
    product_urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]

    # Step 3: Close the search results page before opening any product pages
    page.close()
    print("Closed search results page.")

    # Step 4: Open each product page one by one
    for url in product_urls:
        full_url = "https:" + url
        print(f"Opening product page: {full_url}")

        page = browser.new_page()  # Open a new page for each product
        page.goto(full_url, timeout=60000)

        time.sleep(5)  # Keep the page open for a few seconds (adjust as needed)

        page.close()  # Close current product page before moving to the next
        print(f"Closed product page: {full_url}")

    print("Finished opening all product pages.")
    browser.close()  # Close browser after all pages are visited


with sync_playwright() as p:
    run(p)
