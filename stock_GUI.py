# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData


class StockApp:
    def __init__(self):
        self.stock_list = []

        # Check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

        # Create Window
        self.root = Tk()
        self.root.title("Ashritha Stock Manager")
        self.root.geometry("900x600")

        # Add Menubar
        self.menubar = Menu(self.root)

        # Add File Menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load Data", command=self.load)
        self.filemenu.add_command(label="Save Data", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)

        # Add Web Menu
        self.webmenu = Menu(self.menubar, tearoff=0)
        self.webmenu.add_command(
            label="Scrape Data from Yahoo! Finance...",
            command=self.scrape_web_data
        )
        self.webmenu.add_command(
            label="Import CSV From Yahoo! Finance...",
            command=self.importCSV_web_data
        )

        # Add Chart Menu
        self.chartmenu = Menu(self.menubar, tearoff=0)
        self.chartmenu.add_command(label="Show Chart", command=self.display_chart)

        # Add menus to window
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Web", menu=self.webmenu)
        self.menubar.add_cascade(label="Chart", menu=self.chartmenu)
        self.root.config(menu=self.menubar)

        # Add heading information
        self.headingLabel = Label(
            self.root,
            text="Stock Manager",
            font=("Arial", 18, "bold")
        )
        self.headingLabel.pack(pady=10)

        # Main frame
        self.mainFrame = Frame(self.root)
        self.mainFrame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Add stock list
        self.leftFrame = Frame(self.mainFrame)
        self.leftFrame.pack(side=LEFT, fill=Y, padx=10)

        self.stockListLabel = Label(self.leftFrame, text="Stocks")
        self.stockListLabel.pack()

        self.stockList = Listbox(self.leftFrame, width=20, height=20)
        self.stockList.pack(fill=Y)
        self.stockList.bind("<<ListboxSelect>>", self.update_data)

        # Add Tabs
        self.tabControl = ttk.Notebook(self.mainFrame)

        self.mainTab = Frame(self.tabControl)
        self.historyTab = Frame(self.tabControl)
        self.reportTab = Frame(self.tabControl)

        self.tabControl.add(self.mainTab, text="Main")
        self.tabControl.add(self.historyTab, text="History")
        self.tabControl.add(self.reportTab, text="Report")

        self.tabControl.pack(side=RIGHT, fill=BOTH, expand=True)

        # Set Up Main Tab
        Label(self.mainTab, text="Add Stock", font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        Label(self.mainTab, text="Symbol").grid(row=1, column=0, sticky=E, padx=5, pady=5)
        self.addSymbolEntry = Entry(self.mainTab)
        self.addSymbolEntry.grid(row=1, column=1, padx=5, pady=5)

        Label(self.mainTab, text="Name").grid(row=2, column=0, sticky=E, padx=5, pady=5)
        self.addNameEntry = Entry(self.mainTab)
        self.addNameEntry.grid(row=2, column=1, padx=5, pady=5)

        Label(self.mainTab, text="Shares").grid(row=3, column=0, sticky=E, padx=5, pady=5)
        self.addSharesEntry = Entry(self.mainTab)
        self.addSharesEntry.grid(row=3, column=1, padx=5, pady=5)

        Button(self.mainTab, text="Add Stock", command=self.add_stock).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        Label(self.mainTab, text="Update Shares", font=("Arial", 14, "bold")).grid(
            row=5, column=0, columnspan=2, pady=20
        )

        Label(self.mainTab, text="Shares").grid(row=6, column=0, sticky=E, padx=5, pady=5)
        self.updateSharesEntry = Entry(self.mainTab)
        self.updateSharesEntry.grid(row=6, column=1, padx=5, pady=5)

        Button(self.mainTab, text="Buy Shares", command=self.buy_shares).grid(
            row=7, column=0, pady=10
        )

        Button(self.mainTab, text="Sell Shares", command=self.sell_shares).grid(
            row=7, column=1, pady=10
        )

        Button(self.mainTab, text="Delete Stock", command=self.delete_stock).grid(
            row=8, column=0, columnspan=2, pady=10
        )

        # Setup History Tab
        self.dailyDataList = Text(self.historyTab, width=70, height=25)
        self.dailyDataList.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Setup Report Tab
        self.stockReport = Text(self.reportTab, width=70, height=25)
        self.stockReport.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Call MainLoop
        self.root.mainloop()

    # Load stocks and history from database
    def load(self):
        self.stockList.delete(0, END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)

        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)

        messagebox.showinfo("Load Data", "Data Loaded")

    # Save stocks and history to database
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data", "Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        if self.stockList.curselection():
            self.display_stock_data()

    # Display stock price and volume history
    def display_stock_data(self):
        if not self.stockList.curselection():
            return

        symbol = self.stockList.get(self.stockList.curselection())

        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel["text"] = stock.name + " - " + str(stock.shares) + " Shares"

                self.dailyDataList.delete("1.0", END)
                self.stockReport.delete("1.0", END)

                self.dailyDataList.insert(END, "- Date -        - Price -        - Volume -\n")
                self.dailyDataList.insert(END, "============================================\n")

                total_value = 0

                for daily_data in stock.DataList:
                    row = (
                        daily_data.date.strftime("%m/%d/%y")
                        + "        "
                        + "${:0,.2f}".format(daily_data.close)
                        + "        "
                        + str(daily_data.volume)
                        + "\n"
                    )

                    self.dailyDataList.insert(END, row)
                    total_value = daily_data.close * stock.shares

                # Display report
                self.stockReport.insert(END, "Stock Report\n")
                self.stockReport.insert(END, "==============================\n")
                self.stockReport.insert(END, "Symbol: " + stock.symbol + "\n")
                self.stockReport.insert(END, "Name: " + stock.name + "\n")
                self.stockReport.insert(END, "Shares: " + str(stock.shares) + "\n")

                if len(stock.DataList) > 0:
                    latest_data = stock.DataList[-1]
                    self.stockReport.insert(
                        END,
                        "Latest Price: " + "${:0,.2f}".format(latest_data.close) + "\n"
                    )
                    self.stockReport.insert(
                        END,
                        "Current Value: " + "${:0,.2f}".format(total_value) + "\n"
                    )
                    self.stockReport.insert(
                        END,
                        "Latest Date: " + latest_data.date.strftime("%m/%d/%y") + "\n"
                    )
                else:
                    self.stockReport.insert(END, "No daily data available.\n")

    # Add new stock to track
    def add_stock(self):
        try:
            new_stock = Stock(
                self.addSymbolEntry.get().upper(),
                self.addNameEntry.get(),
                float(self.addSharesEntry.get())
            )

            self.stock_list.append(new_stock)
            self.stockList.insert(END, self.addSymbolEntry.get().upper())

            self.addSymbolEntry.delete(0, END)
            self.addNameEntry.delete(0, END)
            self.addSharesEntry.delete(0, END)

            messagebox.showinfo("Add Stock", "Stock Added")

        except:
            messagebox.showerror("Input Error", "Please enter valid stock information.")

    # Buy shares of stock
    def buy_shares(self):
        if not self.stockList.curselection():
            messagebox.showerror("Selection Error", "Please select a stock.")
            return

        symbol = self.stockList.get(self.stockList.curselection())

        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel["text"] = stock.name + " - " + str(stock.shares) + " Shares"

        messagebox.showinfo("Buy Shares", "Shares Purchased")
        self.updateSharesEntry.delete(0, END)
        self.display_stock_data()

    # Sell shares of stock
    def sell_shares(self):
        if not self.stockList.curselection():
            messagebox.showerror("Selection Error", "Please select a stock.")
            return

        symbol = self.stockList.get(self.stockList.curselection())

        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel["text"] = stock.name + " - " + str(stock.shares) + " Shares"

        messagebox.showinfo("Sell Shares", "Shares Sold")
        self.updateSharesEntry.delete(0, END)
        self.display_stock_data()

    # Remove stock and all history from being tracked
    def delete_stock(self):
        if not self.stockList.curselection():
            messagebox.showerror("Selection Error", "Please select a stock.")
            return

        symbol = self.stockList.get(self.stockList.curselection())

        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stock_list.remove(stock)
                break

        self.stockList.delete(self.stockList.curselection())
        self.headingLabel["text"] = "Stock Manager"
        self.dailyDataList.delete("1.0", END)
        self.stockReport.delete("1.0", END)

        messagebox.showinfo("Delete Stock", "Stock Deleted")

    # Get data from web scraping
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring(
            "Starting Date",
            "Enter Starting Date (m/d/yy)"
        )

        dateTo = simpledialog.askstring(
            "Ending Date",
            "Enter Ending Date (m/d/yy)"
        )

        try:
            stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
        except:
            messagebox.showerror(
                "Cannot Get Data from Web",
                "Check Path for Chrome Driver"
            )
            return

        self.display_stock_data()
        messagebox.showinfo("Get Data From Web", "Data Retrieved")

    # Import CSV stock history file
    def importCSV_web_data(self):
        if not self.stockList.curselection():
            messagebox.showerror("Selection Error", "Please select a stock first.")
            return

        symbol = self.stockList.get(self.stockList.curselection())

        filename = filedialog.askopenfilename(
            title="Select " + symbol + " File to Import",
            filetypes=[("Yahoo Finance CSV", "*.csv")]
        )

        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list, symbol, filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete", symbol + " Import Complete")

    # Display stock price chart
    def display_chart(self):
        if not self.stockList.curselection():
            messagebox.showerror("Selection Error", "Please select a stock first.")
            return

        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list, symbol)


def main():
    app = StockApp()


if __name__ == "__main__":
    main()