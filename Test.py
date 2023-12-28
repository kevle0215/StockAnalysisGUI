import tkinter as tk
import SupportResistance
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
#
# root = tk.Tk()
# fig, ax = plt.subplots()
#
# left_frame = tk.Frame(root, width=500, height=800)
# right_frame = tk.Frame(root, width=1100, height=800)
#
# left_frame.grid(row=0, column=0, sticky="nsew")
# right_frame.grid(row=0, column=1, sticky="nsew")
#
# label = tk.Label(text="HI")
# label.pack()
#
# canvas = FigureCanvasTkAgg(fig, master=left_frame)
# canvas.get_tk_widget().pack()
#
# left_frame.pack()
# right_frame.pack()
#
# # Create a frame with grid layout
# frame = ttk.Frame(root)
# frame.grid(row=0, column=0, padx=10, pady=10)
#
# # Create a plot
# fig, ax = plt.subplots()
# ax.plot([1, 2, 3, 4], [10, 5, 20, 15])
#
# # Embed the plot inside the frame using FigureCanvasTkAgg
# canvas = FigureCanvasTkAgg(fig, master=frame)
# canvas_widget = canvas.get_tk_widget()
# canvas_widget.grid(row=0, column=0)
#
# root.mainloop()

data = yf.download('AMC', start='2022-11-03', end='2023-11-03', interval='1d')
ohlc = data[['Open', 'High', 'Low', 'Close']].copy()
ohlc.reset_index(inplace=True)

print(data.columns)
print(ohlc.columns)
print(ohlc)
print(yf.download('AMC', start='2022-11-03', end='2023-11-03', interval='1d'))

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plot in a Grid Layout")

        # Create a frame with grid layout
        frame = ttk.Frame(root)
        frame.grid(row=0, column=0, padx=10, pady=10)

        # Create a plot
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4], [10, 5, 20, 15])

        # Embed the plot inside the frame using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MyApp(root)
#     root.mainloop()

