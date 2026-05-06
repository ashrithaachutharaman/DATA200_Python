# stock_data.py

import time
import pandas as pd
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def create_driver():
    """
    Creates and returns a Chrome Selenium driver.
    Selenium Manager should automatically handle ChromeDriver.
    """

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    return driver


def get_stock_price(symbol):
    """
    Gets the current stock price from Yahoo Finance using Selenium.
    """

    symbol = symbol.upper()
    driver = None

    try:
        driver = create_driver()

        url = f"https://finance.yahoo.com/quote/{symbol}"
        print(f"Opening: {url}")

        driver.get(url)
        time.sleep(7)

        possible_selectors = [
            'fin-streamer[data-field="regularMarketPrice"]',
            '[data-testid="qsp-price"]',
            'span[data-testid="qsp-price"]'
        ]

        price = ""

        for selector in possible_selectors:
            try:
                price_element = driver.find_element(By.CSS_SELECTOR, selector)

                price = price_element.text.strip()

                if price == "":
                    price = driver.execute_script(
                        "return arguments[0].textContent;",
                        price_element
                    ).strip()

                if price != "":
                    break

            except:
                continue

        driver.quit()

        if price != "":
            return price
        else:
            return "Stock not found."

    except Exception as e:
        print("Could not retrieve data from web.")
        print("Error:", e)

        if driver:
            driver.quit()

        return "Stock not found."


def get_historical_stock_data(symbol, days=30):
    """
    Scrapes historical stock prices from Yahoo Finance for a given stock symbol.
    Returns a pandas DataFrame with Date and Close columns.
    """

    symbol = symbol.upper()
    driver = None

    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        period1 = int(start_date.timestamp())
        period2 = int(end_date.timestamp())

        url = (
            f"https://finance.yahoo.com/quote/{symbol}/history/"
            f"?period1={period1}&period2={period2}"
        )

        driver = create_driver()

        print(f"Opening historical data page: {url}")
        driver.get(url)

        time.sleep(8)

        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

        historical_data = []

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")

            if len(columns) >= 6:
                date = columns[0].text.strip()
                close_price = columns[4].text.strip()
                volume = columns[6].text.strip() if len(columns) >= 7 else "0"

                cleaned_close = close_price.replace(",", "").replace(".", "")
                cleaned_volume = volume.replace(",", "")

                if cleaned_close.isdigit():
                    if cleaned_volume.isdigit():
                        volume_value = int(cleaned_volume)
                    else:
                        volume_value = 0

                    historical_data.append(
                        {
                            "Date": date,
                            "Close": float(close_price.replace(",", "")),
                            "Volume": volume_value
                        }
                    )

        driver.quit()

        if not historical_data:
            print("No historical data found.")
            return None

        df = pd.DataFrame(historical_data)

        df = df.iloc[::-1].reset_index(drop=True)

        return df

    except Exception as e:
        print("Could not retrieve historical stock data.")
        print("Error:", e)

        if driver:
            driver.quit()

        return None


def load_stock_csv(file_path):
    """
    Loads stock data from a CSV file.

    Required columns:
        Date
        Close

    Optional column:
        Volume
    """

    try:
        df = pd.read_csv(file_path)

        if "Date" not in df.columns:
            print("CSV must contain a Date column.")
            return None

        if "Close" not in df.columns:
            print("CSV must contain a Close column.")
            return None

        if "Volume" not in df.columns:
            df["Volume"] = 0

        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce").fillna(0).astype(int)

        df = df.dropna(subset=["Close"])

        return df

    except Exception as e:
        print("Could not import CSV file.")
        print("Check the file path and CSV format.")
        print("Error:", e)
        return None


def get_sample_stock_data():
    """
    Creates sample stock data so the lab can still run
    even if web scraping or CSV import fails.
    """

    data = {
        "Date": [
            "2024-01-01",
            "2024-01-02",
            "2024-01-03",
            "2024-01-04",
            "2024-01-05"
        ],
        "Close": [
            185.64,
            186.20,
            184.75,
            187.10,
            188.35
        ],
        "Volume": [
            1000000,
            1200000,
            900000,
            1100000,
            1300000
        ]
    }

    df = pd.DataFrame(data)
    return df