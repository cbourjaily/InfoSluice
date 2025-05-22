from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

def scrape_soko_glam():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://sokoglam.com/collections/soko-glam-best-of-beauty-awards", timeout=60000)
        page.wait_for_selector(".product-tile", timeout=60000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    products = []

    for product in soup.select(".product-tile"):
        name = product.select_one(".product-title")
        price = product.select_one(".price-item--regular")
        if name and price:
            products.append({
                "name": name.get_text(strip=True),
                "price": price.get_text(strip=True)
            })

    df = pd.DataFrame(products)
    print(df)

if __name__ == "__main__":
    scrape_soko_glam()
