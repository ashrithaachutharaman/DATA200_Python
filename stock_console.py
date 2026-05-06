# stock_console.py

import stock_data
import matplotlib.pyplot as plt


stocks = {}
daily_data = {}


def manage_stocks():
    while True:
        print("\n--- Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")

        choice = input("Enter Menu Option: ")

        if choice == "1":
            add_stock()
        elif choice == "2":
            update_shares()
        elif choice == "3":
            delete_stock()
        elif choice == "4":
            list_stocks()
        elif choice == "0":
            break
        else:
            print("Invalid option. Try again.")


def add_stock():
    symbol = input("Enter stock symbol: ").upper()
    name = input("Enter company name: ")
    shares = int(input("Enter number of shares: "))

    stocks[symbol] = {
        "name": name,
        "shares": shares
    }

    if symbol not in daily_data:
        daily_data[symbol] = []

    print(f"{symbol} was added successfully.")


def update_shares():
    symbol = input("Enter stock symbol to update: ").upper()

    if symbol in stocks:
        shares = int(input("Enter new number of shares: "))
        stocks[symbol]["shares"] = shares
        print(f"{symbol} shares updated successfully.")
    else:
        print("Stock not found.")


def delete_stock():
    symbol = input("Enter stock symbol to delete: ").upper()

    if symbol in stocks:
        del stocks[symbol]

        if symbol in daily_data:
            del daily_data[symbol]

        print(f"{symbol} was deleted successfully.")
    else:
        print("Stock not found.")


def list_stocks():
    if not stocks:
        print("No stocks have been added yet.")
        return

    print("\n--- Current Stocks ---")
    for symbol, info in stocks.items():
        print(f"{symbol} - {info['name']} - {info['shares']} shares")


def add_daily_stock_data():
    symbol = input("Enter stock symbol: ").upper()

    if symbol not in stocks:
        print("Stock not found. Add the stock first using Manage Stocks.")
        return

    date = input("Enter date (YYYY-MM-DD): ")

    print("\nScraping current stock price from Yahoo Finance...")
    scraped_price = stock_data.get_stock_price(symbol)

    if scraped_price is None or scraped_price == "" or scraped_price == "Stock not found.":
        print("Could not scrape stock price.")
        price = float(input("Enter price manually: "))
    else:
        print(f"Scraped price for {symbol}: {scraped_price}")

        cleaned_price = scraped_price.replace(",", "").replace("$", "").strip()

        try:
            price = float(cleaned_price)
        except ValueError:
            print("Scraped price could not be converted to a number.")
            price = float(input("Enter price manually: "))

    volume = int(input("Enter volume: "))

    stock_entry = {
        "date": date,
        "price": price,
        "volume": volume
    }

    daily_data[symbol].append(stock_entry)

    print(f"\nDaily stock data added for {symbol}.")
    print(f"Date: {date}")
    print(f"Price: {price}")
    print(f"Volume: {volume}")


def import_csv_data():
    symbol = input("Enter stock symbol for this CSV data: ").upper()

    if symbol not in stocks:
        print("Stock not found. Add the stock first using Manage Stocks.")
        return

    file_path = input("Enter CSV file name or path: ")

    df = stock_data.load_stock_csv(file_path)

    if df is None or df.empty:
        print("CSV import failed or file had no usable rows.")
        return

    for _, row in df.iterrows():
        stock_entry = {
            "date": str(row["Date"]),
            "price": float(row["Close"]),
            "volume": int(row["Volume"])
        }

        daily_data[symbol].append(stock_entry)

    print(f"\nImported {len(df)} rows of CSV data for {symbol}.")
    print(df)


def show_report():
    if not stocks:
        print("No stocks available. Add stocks first.")
        return

    print("\n--- Stock Report ---")

    for symbol, info in stocks.items():
        print(f"\nStock: {symbol}")
        print(f"Company: {info['name']}")
        print(f"Shares: {info['shares']}")

        if symbol in daily_data and daily_data[symbol]:
            latest_entry = daily_data[symbol][-1]
            latest_price = latest_entry["price"]
            total_value = latest_price * info["shares"]

            print(f"Latest Date: {latest_entry['date']}")
            print(f"Latest Price: ${latest_price:.2f}")
            print(f"Latest Volume: {latest_entry['volume']}")
            print(f"Total Value: ${total_value:.2f}")
        else:
            print("No daily data available yet.")


def show_chart():
    print("\n--- Show Chart ---")
    print("1 - Chart from scraped historical web data")
    print("2 - Chart from stored daily data / imported CSV data")

    choice = input("Enter chart option: ")

    symbol = input("Enter stock symbol for chart: ").upper()

    if choice == "1":
        try:
            days = int(input("Enter number of days to chart, like 30, 60, or 90: "))
        except ValueError:
            print("Invalid number of days. Using 30 days.")
            days = 30

        print(f"\nScraping historical data for {symbol} over the last {days} days...")

        df = stock_data.get_historical_stock_data(symbol, days)

        if df is None or df.empty:
            print("No historical data available for this stock.")
            return

        print("\nHistorical Data:")
        print(df)

        plt.figure(figsize=(12, 6))
        plt.plot(df["Date"], df["Close"], marker="o")

        plt.title(f"{symbol} Stock Closing Price Over Last {days} Days")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    elif choice == "2":
        if symbol not in daily_data or not daily_data[symbol]:
            print("No stored or imported daily data available for this stock.")
            return

        dates = []
        prices = []

        for entry in daily_data[symbol]:
            dates.append(entry["date"])
            prices.append(entry["price"])

        plt.figure(figsize=(12, 6))
        plt.plot(dates, prices, marker="o")

        plt.title(f"{symbol} Stock Price from Stored / CSV Data")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    else:
        print("Invalid chart option.")


def manage_data():
    while True:
        print("\n--- Manage Data ---")
        print("1 - Save Data")
        print("2 - Load Data")
        print("3 - Retrieve Data")
        print("4 - Import Daily Stock Data from CSV")
        print("0 - Exit Manage Data")

        choice = input("Enter Menu Option: ")

        if choice == "1":
            save_data()
        elif choice == "2":
            load_data()
        elif choice == "3":
            retrieve_data()
        elif choice == "4":
            import_csv_data()
        elif choice == "0":
            break
        else:
            print("Invalid option. Try again.")


def save_data():
    with open("stock_data_saved.txt", "w") as file:
        file.write(str(stocks))
        file.write("\n")
        file.write(str(daily_data))

    print("Data saved to stock_data_saved.txt.")


def load_data():
    print("Load feature placeholder.")
    print("For this version, CSV import is handled through option 4 under Manage Data.")


def retrieve_data():
    print("\n--- Retrieved Data ---")
    print("Stocks:")
    print(stocks)
    print("\nDaily Data:")
    print(daily_data)


def main():
    while True:
        print("\n--- Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data using Web Scraping")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve, Import CSV)")
        print("0 - Exit Program")

        choice = input("Enter Menu Option: ")

        if choice == "1":
            manage_stocks()
        elif choice == "2":
            add_daily_stock_data()
        elif choice == "3":
            show_report()
        elif choice == "4":
            show_chart()
        elif choice == "5":
            manage_data()
        elif choice == "0":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()