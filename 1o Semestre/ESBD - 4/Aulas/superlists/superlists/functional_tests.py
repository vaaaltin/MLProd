from selenium import webdriver

browser = webdriver.Chrome()
browser.get("http://localhost:8000")

assert 'worked successfully' in browser.title