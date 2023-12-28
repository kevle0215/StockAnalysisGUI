import tkinter as tk
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import mplcursors
from matplotlib.patches import Rectangle
import SupportResistance
import matplotlib.colors as mcolors


def open_new_window(master, stock_name, start_date, end_date, interval):

    # create new window
    newWindow = tk.Toplevel(master)
    newWindow.title(stock_name + " Stock Chart")

    # blank stock chart creation
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    chart_canvas = FigureCanvasTkAgg(fig, master=newWindow)
    chart_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # create toolbar
    toolbar = NavigationToolbar2Tk(chart_canvas, newWindow)
    toolbar.update()
    chart_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # fill stock chart with data
    stock_chart_with_scrollbar(stock_name, start_date, end_date, interval, ax)

    # place cursor on stock chart
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"{mdates.num2date(sel.target[0]).strftime('%Y-%m-%d %H:%M:%S')}\nPrice: {sel.target[1]:.2f}"))


def stock_chart_with_scrollbar(symbol, start_date, end_date, interval, ax):

    # price data
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

    ohlc = data[['Open', 'High', 'Low', 'Close']].copy()
    ohlc.reset_index(inplace=True)
    ohlc['Date'] = ohlc['Date'].map(mdates.date2num)

    # candlestick chart setup
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='g', colordown='r')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title(f"Candlestick Chart for {symbol}")

    # format x-axis as dates
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    support_resistance_graph(symbol, start_date, end_date, interval, ax, ohlc)


def support_resistance_graph(symbol, start_date, end_date, interval, ax, data):
    srArray = SupportResistance.support_resistance(symbol, start_date, end_date, interval)

    for sr in srArray:

        date_1 = find_date(data, sr[0])
        date_2 = find_date(data, sr[1])

        zone = Rectangle((min(date_1, date_2), sr[0]), max(date_1, date_2) - min(date_1, date_2),
                         sr[1]-sr[0], fc=mcolors.to_rgba('red', 0.5))
        ax.add_patch(zone)


def find_date(data, target_price):

    filtered_data = data[(data['Close'] == target_price) |
                         (data['Open'] == target_price) |
                         (data['High'] == target_price) |
                         (data['Low'] == target_price)]
    priceDate = min(filtered_data['Date'].values)

    return priceDate
