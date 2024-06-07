from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class CoinMarketCapScraper:
    def __init__(self):
        self.base_url = "https://coinmarketcap.com/currencies/"
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def scrape_coin_data(self, coin):
        coin_url = f"{self.base_url}{coin.lower()}"
        self.driver.get(coin_url)
        time.sleep(5)  # Let the page load completely

        data = {}

        # Scraping price
        price_element = self.driver.find_element_by_xpath("//span[@class='priceValue___11gHJ']")
        data["price"] = float(price_element.text.strip().replace("$", "").replace(",", ""))

        # Scraping price change
        price_change_element = self.driver.find_element_by_xpath("//span[@class='sc-15yy2pl-0 hZxUBB']")
        data["price_change"] = float(price_change_element.text.strip().split()[0])

        # Scraping market cap
        market_cap_element = self.driver.find_element_by_xpath("//div[contains(text(), 'Market Cap')]/following-sibling::div")
        data["market_cap"] = int(market_cap_element.text.strip().replace("$", "").replace(",", ""))

        # Scraping volume
        volume_element = self.driver.find_element_by_xpath("//div[contains(text(), 'Volume (24h)')]/following-sibling::div")
        data["volume"] = int(volume_element.text.strip().replace("$", "").replace(",", ""))

        # Scraping circulating supply
        circulating_supply_element = self.driver.find_element_by_xpath("//div[contains(text(), ' Circulating Supply')]/following-sibling::div")
        data["circulating_supply"] = int(circulating_supply_element.text.strip().replace(",", ""))

        # Scraping total supply
        total_supply_element = self.driver.find_element_by_xpath("//div[contains(text(), 'Total Supply')]/following-sibling::div")
        data["total_supply"] = int(total_supply_element.text.strip().replace(",", ""))

        return data

    def close_driver(self):
        self.driver.quit()
