import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
try:
    # Replace this with an element that should appear after the page loads completely
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.some-class-or-id"))  # Example CSS Selector
    )
    time.sleep(5)  # Optional: wait for some additional time to ensure m3u8 URLs load
except Exception as e:
    print(f"Error: {e}")

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

# Write the M3U playlist to a file
if m3u8_urls:
    with open('playlist.m3u', 'w') as f:
        for m3u8_url in m3u8_urls:
            # Extract the channel name from the URL (you can customize this if needed)
            channel_name = m3u8_url.split("/")[-2]  # Channel name based on URL structure
            f.write(f'#EXTINF:-1, {channel_name} \n')
            f.write(f'#EXTVLCOPT:http-user-agent=Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc\n')
            f.write(f'#EXTHTTP:{{"cookie":"{edge_cache_cookie}"}}\n')
            f.write(f'{m3u8_url}\n\n')
    print("M3U playlist updated and saved to 'playlist.m3u'")
else:
    print("No m3u8 URLs found.")

# Close the WebDriver
driver.quit()
