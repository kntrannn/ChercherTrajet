import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
from tkcalendar import DateEntry
from Controller.TripController import update_planned_trip, get_all_countries_without_chosen, get_country_name

class UpdateTripWindow(tk.Toplevel):
    """
    A window for modifying a planned trip.

    Args:
        master: The master widget.
        trip: The trip to modify.

    Attributes:
        master: The master widget.
        user: The current user object.
        trip: The trip to modify.
        list_countries: A list of countries excluding the departure country.
        background_image: The background image for the window.
        canvas: Canvas widget for the background image.
        title1: Customized label for the title.
        label1: Customized label for "Choose your departure country".
        departure_country: Combo box for selecting the departure country.
        label2: Customized label for "Choose the destination country".
        destination_country: Combo box for selecting the destination country.
        label3: Customized label for "Choose the departure date".
        departure_date: Date picker for selecting the departure date.
        label4: Customized label for "Choose the return date".
        return_date: Date picker for selecting the return date.
        label5: Customized label for "Choose the transport".
        transport: Combo box for selecting the mode of transport.
        label6: Customized label for "Duration (in hours)".
        duration: Entry widget for entering the duration of the trip.
        button1: Customized button for saving the trip.
    """
    def __init__(self, master, trip):
        ctk.set_appearance_mode("light")
        super().__init__()
        self.master = master
        self.user = master.user
        self.trip = trip
        self.title("Modify trip")
        self.resizable(False, False)
        self.config(bg = "#f5f6f9")

        self.list_countries = get_all_countries_without_chosen(None)
        
        # Load the background image
        self.background_image = tk.PhotoImage(file="View/pictures/bg_map.png")
        
        # Create a canvas and set the background image
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Title
        self.title1 = ctk.CTkLabel(self, text="Modify your trip", font = ("Impact", 25), text_color='#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 50, window=self.title1)

        # Label entry for the home country
        self.label1 = ctk.CTkLabel(self, text="Choose your departure country", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 80, window=self.label1)

        # Combo box for the departure country
        self.departure_country = ttk.Combobox(self, font=("Arial", 11, 'bold'), values=self.list_countries)
        self.departure_country.configure(state="readonly")
        self.departure_country.set("")
        self.departure_country.set(get_country_name(trip.departure_id))
        self.canvas.create_window(250, 110, window=self.departure_country)

        # Label entry for the destination country
        self.label2 = ctk.CTkLabel(self, text="Choose the destination country", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 140, window=self.label2)

        # Combo box for the destination country
        self.destination_country = ttk.Combobox(self, font=("Arial", 11, 'bold'), values=self.list_countries)
        self.destination_country.configure(state="readonly")
        self.destination_country.set("")
        self.destination_country.set(get_country_name(trip.destination_id))
        self.canvas.create_window(250, 170, window=self.destination_country)

        # Label entry for the departure date
        self.label3 = ctk.CTkLabel(self, text="Choose the departure date", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 200, window=self.label3)

        # Date picker for the departure date
        self.departure_date = DateEntry(self, date_pattern="dd/mm/yyyy")
        self.departure_date.configure(state="readonly")
        self.departure_date.set_date(trip.departure_date)
        self.canvas.create_window(250, 230, window=self.departure_date)

        # Label entry for the return date
        self.label4 = ctk.CTkLabel(self, text="Choose the return date", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 260, window=self.label4)

        # Date picker for the return date
        self.return_date = DateEntry(self, date_pattern="dd/mm/yyyy")
        self.return_date.configure(state="readonly")
        self.return_date.set_date(trip.return_date)
        self.canvas.create_window(250, 290, window=self.return_date)

        # Combo box for the transport
        self.label5 = ctk.CTkLabel(self, text="Choose the transport", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 320, window=self.label5)
        self.transport = ttk.Combobox(self, font=("Arial", 11, 'bold'), values=["Plane", "Train", "Car", "Bus", "Ferry", "Bike", "Foot"])
        self.transport.configure(state="readonly")
        self.transport.set(trip.transport)
        self.canvas.create_window(250, 350, window=self.transport)

        # Entry for duration (in hours)
        self.label6 = ctk.CTkLabel(self, text="Duration (in hours)", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 380, window=self.label6)
        self.duration = ctk.CTkEntry(self, font=("Arial", 11, 'bold'))
        self.duration.insert(0, str(trip.duration))
        self.canvas.create_window(250, 410, window=self.duration)

        # Button to save the trip
        self.button1 = ctk.CTkButton(self, text="Modify your trip", font = ("Arial", 11, 'bold'), width = 200, height = 30, fg_color= '#354f52', corner_radius = 10, command=self.update_trip)
        self.canvas.create_window(250, 460, window=self.button1)

        self.mainloop()

    def update_trip(self):
        """Update the trip in the database."""
        departure_country = self.departure_country.get()
        destination_country = self.destination_country.get()
        departure_date = self.departure_date.get_date()
        return_date = self.return_date.get_date()
        transport = self.transport.get()
        duration = self.duration.get()

        # Convert the date to a string
        departure_date = departure_date.strftime("%Y-%m-%d")
        return_date = return_date.strftime("%Y-%m-%d")

        # Convert the date to a datetime object
        departure_date = datetime.strptime(departure_date, "%Y-%m-%d")
        return_date = datetime.strptime(return_date, "%Y-%m-%d")

        is_valid, message = update_planned_trip(self.trip, departure_country, destination_country, departure_date, return_date, transport, duration)

        if not is_valid:
            messagebox.showerror("Error", message)
            self.lift()
        else:
            messagebox.showinfo("Success", message)
            self.destroy()

            # Refresh the map
            self.master.master.draw()

            # Refresh the window
            from View.ShowAllTripsWindow import ShowAllTripsWindow
            ShowAllTripsWindow(self.master.master)