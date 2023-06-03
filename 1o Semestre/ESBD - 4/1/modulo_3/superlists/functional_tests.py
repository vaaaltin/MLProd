from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
# chrome_options.add_argument("--no-sandbox")

browser = webdriver.Chrome(options=chrome_options)
browser.get("http://localhost:8000")

assert 'worked successfully' in browser.title