import tkinter as tk
import SupportResistance
import StockChartWindow
import AnalysisButton


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
        self.touches_var = tk.StringVar()

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
        sensitivity_label = tk.Label(left_frame, text="Sensitivity:")
        touches_label = tk.Label(left_frame, text="Number of Touches:")

        # entry widgets
        symbol_entry = tk.Entry(left_frame, textvariable=self.symbol_var)
        startdate_entry = tk.Entry(left_frame, textvariable=self.start_date_var)
        enddate_entry = tk.Entry(left_frame, textvariable=self.end_date_var)
        interval_entry = tk.Entry(left_frame, textvariable=self.interval_var)
        touches_entry = tk.Entry(left_frame, textvariable=self.touches_var)

        # buttons
        analysis_button = tk.Button(left_frame, text='Analyze',
                                    command=lambda: AnalysisButton.analyze(
                                        self.symbol_var.get(),
                                        self.start_date_var.get(),
                                        self.end_date_var.get(),
                                        self.interval_var.get(),
                                        self.touches_var.get(),
                                        sensitivity_slider.get(),
                                        sr_output
                                    ))

        stockgraph_button = tk.Button(left_frame, text='Plot Stock Prices',
                                      command=lambda: StockChartWindow.open_new_window(
                                          self.root,
                                          self.symbol_var.get(),
                                          self.start_date_var.get(),
                                          self.end_date_var.get(),
                                          self.interval_var.get(),
                                          self.touches_var.get(),
                                          sensitivity_slider.get()
                                      ))

        # slider
        sensitivity_slider = tk.Scale(left_frame, from_=0, to=4, orient=tk.HORIZONTAL)

        # LEFT FRAME WIDGET LOCATIONS #
        # labels
        symbol_label.grid(row=0, columnspan=1, column=0)
        startdate_label.grid(row=1, columnspan=1, column=0)
        enddate_label.grid(row=2, columnspan=1, column=0)
        interval_label.grid(row=3, columnspan=1, column=0)
        touches_label.grid(row=4, columnspan=1, column=0)
        sensitivity_label.grid(row=5, columnspan=1, column=0)

        # entry widgets
        symbol_entry.grid(row=0, columnspan=1, column=1)
        startdate_entry.grid(row=1, columnspan=1, column=1)
        enddate_entry.grid(row=2, columnspan=1, column=1)
        interval_entry.grid(row=3, columnspan=1, column=1)
        touches_entry.grid(row=4, columnspan=1, column=1)

        # buttons
        analysis_button.grid(row=6, columnspan=2, column=0)
        stockgraph_button.grid(row=7, columnspan=2, column=0)

        # slider
        sensitivity_slider.grid(row=5, columnspan=1, column=1)

        # RIGHT FRAME WIDGET SETUP
        # textbox
        sr_output = tk.Text(right_frame, height=20, width=35, wrap=tk.WORD)

        # scrollbar
        output_scrollbar = tk.Scrollbar(right_frame)

        # RIGHT FRAME WIDGET LOCATIONS
        # textbox
        sr_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sr_output.config(yscrollcommand=output_scrollbar.set)

        # scrollbar
        output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        output_scrollbar.config(command=sr_output.yview)


StockAnalysisApp()
