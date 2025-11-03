from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pathlib

# Path to your local HTML file
html_path = pathlib.Path("weather.html").resolve().as_uri()   # converts to file:// URL

width = 800
height = 480

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(f"--window-size={width},{height + 139}")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options,
)

try:
    driver.get(html_path)               # load the file
    driver.save_screenshot("screenshot.png")
    print("✅ Screenshot saved as screenshot.png")
finally:
    driver.quit()
