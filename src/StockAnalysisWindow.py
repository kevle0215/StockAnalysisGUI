import tkinter as tk
import SupportResistance
from StockChartWindow import StockChartWindow

class StockAnalysisWindow():
    def __init__(self, master):
        """
        Initializes the StockAnalysisWindow.

        """
        self.master = master
        self.notification_window = tk.Toplevel(self.master)
        self.notification_window.title("Stock Analysis Tool")
        self.notification_window.geometry("600x300")

        self.symbol_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.interval_var = tk.StringVar()
        self.touches_var = tk.StringVar()
        self.sensitivity_var = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Configures the graphical elements of the Stock Analysis Window.
        """
        # Create frames
        left_frame = tk.Frame(self.notification_window, width=200, height=300)
        right_frame = tk.Frame(self.notification_window, width=400, height=300)

        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid(row=0, column=1, sticky="nsew")

        # LEFT FRAME WIDGETS SETUP #
        # Labels
        symbol_label = tk.Label(left_frame, text="Stock Symbol:")
        startdate_label = tk.Label(left_frame, text="Start Date:")
        enddate_label = tk.Label(left_frame, text="End Date:")
        interval_label = tk.Label(left_frame, text="Interval:")
        sensitivity_label = tk.Label(left_frame, text="Sensitivity:")
        touches_label = tk.Label(left_frame, text="Number of Touches:")

        # Entry widgets
        symbol_entry = tk.Entry(left_frame, textvariable=self.symbol_var)
        startdate_entry = tk.Entry(left_frame, textvariable=self.start_date_var)
        enddate_entry = tk.Entry(left_frame, textvariable=self.end_date_var)
        interval_entry = tk.Entry(left_frame, textvariable=self.interval_var)
        touches_entry = tk.Entry(left_frame, textvariable=self.touches_var)

        # Textbox
        sr_output = tk.Text(right_frame, height=20, width=35, wrap=tk.WORD)

        # Buttons
        analysis_button = tk.Button(left_frame, text='Analyze', command=lambda: self.analyze(sr_output))
        stockgraph_button = tk.Button(left_frame, text='Plot Stock Prices', command=lambda: self.open_stock_chart_window())

        # Slider
        sensitivity_slider = tk.Scale(left_frame, from_=0, to=4, orient=tk.HORIZONTAL)

        # LEFT FRAME WIDGET LOCATIONS #
        # Labels
        symbol_label.grid(row=0, columnspan=1, column=0)
        startdate_label.grid(row=1, columnspan=1, column=0)
        enddate_label.grid(row=2, columnspan=1, column=0)
        interval_label.grid(row=3, columnspan=1, column=0)
        touches_label.grid(row=4, columnspan=1, column=0)
        sensitivity_label.grid(row=5, columnspan=1, column=0)

        # Entry widgets
        symbol_entry.grid(row=0, columnspan=1, column=1)
        startdate_entry.grid(row=1, columnspan=1, column=1)
        enddate_entry.grid(row=2, columnspan=1, column=1)
        interval_entry.grid(row=3, columnspan=1, column=1)
        touches_entry.grid(row=4, columnspan=1, column=1)

        # Buttons
        analysis_button.grid(row=6, columnspan=2, column=0)
        stockgraph_button.grid(row=7, columnspan=2, column=0)

        # Slider
        sensitivity_slider.grid(row=5, columnspan=1, column=1)

        # RIGHT FRAME WIDGET SETUP
        # Scrollbar
        output_scrollbar = tk.Scrollbar(right_frame)

        # RIGHT FRAME WIDGET LOCATIONS
        # Textbox
        sr_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sr_output.config(yscrollcommand=output_scrollbar.set)

        # Scrollbar
        output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def open_stock_chart_window(self):
        """
        Opens the StockChartWindow when the "Plot Stock Prices" button is clicked.
        """
        stock_chart_window = StockChartWindow(self.master, self.symbol_var.get(), self.start_date_var.get(),
                                              self.end_date_var.get(), self.interval_var.get(), self.touches_var.get(),
                                              self.sensitivity_var.get())
        stock_chart_window.create_stock_chart()

    def analyze(self, text_box):
        """
        Analyzes the stock data based on user input and displays the results in the Textbox.

        Args:
            text_box (Text): The Textbox widget for displaying analysis results.
        """
        srArray = SupportResistance.support_resistance(self.symbol_var.get(), self.start_date_var.get(),
                                                       self.end_date_var.get(), self.interval_var.get(),
                                                       self.touches_var.get(), self.sensitivity_var.get())

        # analysis text to be displayed in the textbox window
        analysis_text = f"The supports and resistances of the stock {self.symbol_var.get()} are " + \
                        ', '.join([f"({round(sr[0], 2)}, {round(sr[1], 2)})" for sr in srArray])

        text_box.insert(tk.END, analysis_text)

