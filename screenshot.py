from config import screen
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def capture():
    html_path = Path("weather.html").resolve().as_uri()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": screen['width'], "height": screen['height']})
        await page.goto(html_path)
        await page.screenshot(path="screenshot.png")
        await browser.close()
        print("✅ Screenshot saved as screenshot.png")

asyncio.run(capture())
