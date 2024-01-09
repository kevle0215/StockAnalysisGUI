import tkinter as tk
import StockAnalysisWindow
import NotificationWindow

class StockAnalysisApp:
    """
    StockAnalysisApp - A Graphical User Interface (GUI) application for stock analysis and notification management.
    """

    def __init__(self):
        """
        Initializes Stock Analysis App

        Creates the main window, sets its title and geometry, calls the creation of widgets, and starts main event loop.
        """
        self.root = tk.Tk()
        self.root.title("Stock Analysis Tool")
        self.root.geometry("300x100")

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        """
        Configures graphical elements of the main window.

        - analysis_button (Button): Initiates the Individual Stock Analysis window.
        - notification_button (Button): Activates the Notification System window.
        """

        # Individual Stock Analysis button
        analysis_button = tk.Button(self.root, text='Individual Stock Analysis',
                                    command=lambda: StockAnalysisWindow.StockAnalysisWindow(self.root))

        # Notification System button
        notification_button = tk.Button(self.root, text='Notification System',
                                        command=lambda: NotificationWindow.NotificationWindow(self.root))

        # Pack buttons for display in the main window
        analysis_button.pack()
        notification_button.pack()


# Instantiate the StockAnalysisApp to initiate the application
if __name__ == "__main__":
    StockAnalysisApp()
