import os
import csv
import time
from playwright.sync_api import sync_playwright
from rich import print


def save_to_csv(product_title, product_price, product_url, filename):
    """Saves product details to a CSV file."""
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)  # Create folder if not exists
    file_path = os.path.join(output_folder, filename)

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "URL"])
        writer.writerow([product_title, product_price, product_url])

    print(f"Saved: {file_path}")


def run(playwright):
    start_url = "https://www.daraz.com.bd/catalog/?q=router"
    browser = playwright.chromium.launch(headless=False)

    # Step 1: Open search results page ONCE
    page = browser.new_page()
    page.goto(start_url)
    print("Opened search results page.")

    # Step 2: Collect all product links
    links = page.locator("a[href*='tp-link']").all()
    product_urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]

    # Step 3: Close the search results page
    page.close()
    print("Closed search results page.")

    # Step 4: Open each product page, extract data, and save
    for idx, url in enumerate(product_urls):
        full_url = "https:" + url
        print(f"Opening product page: {full_url}")

        page = browser.new_page()

        # Retry mechanism with timeout handling
        try:
            page.goto(full_url, timeout=120000)  # Increase timeout to 2 minutes
            page.wait_for_selector("h1")  # Wait for the product title to appear

            # Extract product details
            title = page.locator("h1").text_content() or "No Title Found"

            # ✅ Fix: Wait for price to appear, then extract
            try:
                price_selector = ".pdp-price"  # ✅ Use correct selector (Inspect in DevTools)
                page.wait_for_selector(price_selector, timeout=10000)
                price = page.locator(price_selector).text_content().strip()
            except:
                price = "No Price Found"

            # Save to CSV file (one file per product)
            filename = f"product_{idx + 1}.csv"
            save_to_csv(title.strip(), price.strip(), full_url, filename)

        except playwright._impl._errors.TimeoutError:
            print(f"Timeout occurred for {full_url}. Skipping this product.")

        time.sleep(2)  # Keep the page open for a few seconds
        page.close()
        print(f"Closed product page: {full_url}")

    browser.close()
    print("Finished scraping all products.")


if __name__ == "__main__":
    with sync_playwright() as p:
        run(p)
