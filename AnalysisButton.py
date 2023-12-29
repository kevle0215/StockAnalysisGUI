import tkinter as tk
import SupportResistance


def analyze(symbol, start_date, end_date, interval, touches, sensitivity, text_box):
    srArray = SupportResistance.support_resistance(symbol, start_date, end_date, interval, touches, sensitivity)

    analysisText = f"The supports and resistances of the stock {symbol} are " + \
                   ', '.join([f"({round(sr[0], 2)}, {round(sr[1], 2)})" for sr in srArray])

    text_box.insert(tk.END, analysisText)


