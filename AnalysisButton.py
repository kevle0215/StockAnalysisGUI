import tkinter as tk
import SupportResistance
import StockChartWindow
from tkinter import ttk
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import DateFormatter, date2num
import datetime
import matplotlib.dates as mdates


def analyze(symbol, start_date, end_date, interval, touches, sensitivity, text_box):
    srArray = SupportResistance.support_resistance(symbol, start_date, end_date, interval, touches, sensitivity)

    analysisText = f"The supports and resistances of the stock {symbol} are " + \
                   ', '.join([f"({round(sr[0], 2)}, {round(sr[1], 2)})" for sr in srArray])

    text_box.insert(tk.END, analysisText)


