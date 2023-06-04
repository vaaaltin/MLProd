from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Setup chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")

browser = webdriver.Chrome()
browser.get("http://localhost:8000")

assert 'worked successfully' in browser.title

