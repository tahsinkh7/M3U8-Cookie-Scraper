import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options and WebDriver
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU for headless mode

# Initialize the Chrome WebDriver with WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the target URL
url = "https://toffeelive.com/en/live"  # Replace with your actual URL
driver.get(url)

# Wait for the page to load completely (adjust time if necessary)
time.sleep(1)

# Scrape the page source
page_source = driver.page_source

# Extract unique m3u8 URLs from the desired domain only
m3u8_urls = list(
    set(
        url for url in re.findall(r'https://[^"]+\.m3u8', page_source)
        if "bldcmprod-cdn.toffeelive.com" in url
    )
)

# Extract the full Edge-Cache-Cookie with its prefix
cookie_match = re.search(r'Edge-Cache-Cookie=([^;\\]+)', page_source)
edge_cache_cookie = f"Edge-Cache-Cookie={cookie_match.group(1)}" if cookie_match else "Edge-Cache-Cookie=Not Available"

# Print the results in the required format
if m3u8_urls:
    for m3u8_url in m3u8_urls:
        print(f"M3U8: {m3u8_url}")
        print(f"Cookie: {edge_cache_cookie}")
        print("")  # Blank line for separation
else:
    print("No M3U8 URLs found from the specified domain.")

# Close the WebDriver
driver.quit()
