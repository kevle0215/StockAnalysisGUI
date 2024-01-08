import sqlite3
import tkinter as tk
from AddSR import AddSR
from Notification import Notification

class NotificationWindow:
    """
    NotificationWindow - GUI window for setting up stock notifications.

    Attributes:
        stock_var (StringVar): Variable to store stock symbol input.
        days_var (IntVar): Variable to store days input.
        touches_var (StringVar): Variable to store number of touches input.
        sensitivity_var (IntVar): Variable to store sensitivity input.
        running_var (StringVar): Variable to store running state input.
    """

    def __init__(self, master):
        """
        Initializes the NotificationWindow.
        """
        self.master = master
        self.notification_window = tk.Toplevel(self.master)
        self.notification_window.title("Set up notifications")

        self.stock_var = tk.StringVar()
        self.days_var = tk.IntVar()
        self.touches_var = tk.StringVar()
        self.sensitivity_var = tk.IntVar()
        self.running_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Configures graphical elements of the notification window.
        """
        # Label setup
        stock_label = tk.Label(self.notification_window, text="Stock Symbol")
        days_label = tk.Label(self.notification_window, text="Days")
        touches_label = tk.Label(self.notification_window, text="Number of Touches")
        sensitivity_label = tk.Label(self.notification_window, text="Sensitivity")

        # Entry setup
        stock_entry = tk.Entry(self.notification_window, textvariable=self.stock_var)
        days_entry = tk.Entry(self.notification_window, textvariable=self.days_var)
        touches_entry = tk.Entry(self.notification_window, textvariable=self.touches_var)

        # Slider
        sensitivity_slider = tk.Scale(self.notification_window, from_=0, to=4, orient=tk.HORIZONTAL,
                                      variable=self.sensitivity_var)
        
        # Buttons
        new_button = tk.Button(self.notification_window, text='Create New Notification',
                               command=lambda: self.new_notification())

        old_button = tk.Button(self.notification_window, text='Delete Notification',
                               command=lambda: self.delete_notification())

        running_button = tk.Button(self.notification_window, text="Start/Stop Notifications",
                                  command=lambda: self.running(self.running_var))

        addSR_button = tk.Button(self.notification_window, text="Manually Add Support/Resistance",
                                 command=lambda: AddSR(self.master))

        # Label locations
        stock_label.grid(column=0, row=0)
        days_label.grid(column=0, row=1)
        touches_label.grid(column=0, row=2)
        sensitivity_label.grid(column=0, row=3)

        # Entry locations
        stock_entry.grid(column=1, row=0)
        days_entry.grid(column=1, row=1)
        touches_entry.grid(column=1, row=2)

        # Slider location
        sensitivity_slider.grid(column=1, columnspan=1, row=3)

        # Button locations
        new_button.grid(column=0, row=4)
        old_button.grid(column=1, row=4)
        addSR_button.grid(column=0, row=5)
        running_button.grid(column=1, columnspan=1, row=5)
    
    def new_notification(self):
        """
        Creates a new notification using user input and performs necessary setup.
        """
        notification = Notification(self.stock_var.get(), self.days_var.get(), self.touches_var.get(), self.sensitivity_var.get())
        notification.calculate_sr()
        notification.boundary_setup()
    
    def delete_notification(self):
        """
        Deletes a notification using user input.
        """
        notification = Notification(self.stock_var.get(), self.days_var.get(), self.touches_var.get(), self.sensitivity_var.get())
        notification.delete_notification()
        
    def running(self, var):
        """
        Toggles the running state of notifications and updates the database.

        Args:
            var (StringVar): The variable storing the running state.
        """
        self.fetch_boolean(var)
        current_value = var.get()

        if current_value == "False":
            var.set("True")
        else:
            var.set("False")

        self.update_boolean(var.get())

    def update_boolean(self, running_var):
        """
        Updates the running state in the database.

        Args:
            running_var (str): The running state to be updated.
        """
        try:
            with sqlite3.connect('stock_data.db') as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE script_state SET running_var=? WHERE id=0', (running_var,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def fetch_boolean(self, running_var):
        """
        Fetches the running state from the database.

        Args:
            running_var (StringVar): The variable to store the fetched running state.
        """
        try:
            with sqlite3.connect('stock_data.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT running_var FROM script_state')
                row = cursor.fetchone()

                if row is not None:
                    running_var.set(row[0])
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Main block to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = NotificationWindow(root)
    root.mainloop()
