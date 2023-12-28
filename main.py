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


class StockAnalysisApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stock Analysis Tool")
        self.root.geometry("600x300")

        # Variables to store user input
        self.symbol_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.interval_var = tk.StringVar()

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        # create frames
        left_frame = tk.Frame(self.root, width=200, height=300)
        right_frame = tk.Frame(self.root, width=400, height=300)

        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid(row=0, column=1, sticky="nsew")

        # LEFT FRAME WIDGETS SETUP #

        # labels
        symbol_label = tk.Label(left_frame, text="Stock Symbol:")
        startdate_label = tk.Label(left_frame, text="Start Date:")
        enddate_label = tk.Label(left_frame, text="End Date:")
        interval_label = tk.Label(left_frame, text="Interval:")

        # entry widgets
        symbol_entry = tk.Entry(left_frame, textvariable=self.symbol_var)
        startdate_entry = tk.Entry(left_frame, textvariable=self.start_date_var)
        enddate_entry = tk.Entry(left_frame, textvariable=self.end_date_var)
        interval_entry = tk.Entry(left_frame, textvariable=self.interval_var)

        # buttons
        analysis_button = tk.Button(left_frame, text='Analyze',
                                    command=lambda: SupportResistance.support_resistance(
                                        self.symbol_var.get(),
                                        self.start_date_var.get(),
                                        self.end_date_var.get(),
                                        self.interval_var.get()
                                    ))

        stockgraph_button = tk.Button(left_frame, text='Plot Stock Prices',
                                      command=lambda: StockChartWindow.open_new_window(
                                          self.root,
                                          self.symbol_var.get(),
                                          self.start_date_var.get(),
                                          self.end_date_var.get(),
                                          self.interval_var.get()))

        # LEFT FRAME WIDGET LOCATIONS #

        # labels
        symbol_label.grid(row=0, columnspan=1, column=0)
        startdate_label.grid(row=1, columnspan=1, column=0)
        enddate_label.grid(row=2, columnspan=1, column=0)
        interval_label.grid(row=3, columnspan=1, column=0)

        # entry widgets
        symbol_entry.grid(row=0, columnspan=1, column=1)
        startdate_entry.grid(row=1, columnspan=1, column=1)
        enddate_entry.grid(row=2, columnspan=1, column=1)
        interval_entry.grid(row=3, columnspan=1, column=1)

        # buttons
        analysis_button.grid(row=4, columnspan=2, column=0)
        stockgraph_button.grid(row=5, columnspan=2, column=0)


StockAnalysisApp()
