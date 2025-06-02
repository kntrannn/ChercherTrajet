import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from Controller.TripController import add_new_trip, get_list_sites_names

class PlanNewTripWindow(tk.Toplevel):
    """
    A window for planning a new trip.

    Args:
        master: The master widget.
        country_destination: The destination country.

    Attributes:
        master: The master widget.
        user: The current user object.
        country_destination: The destination country.
        list_countries: A list of countries excluding the destination country.
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
    def __init__(self, master, site_destination):
        super().__init__()
        self.master = master
        self.user = master.user
        self.sites = master.sites
        self.sites_names = get_list_sites_names(self.sites)
        self.site_destination = site_destination
        self.resizable(False, False)
        self.title("Plan a new trip")

        # Load the background image
        self.background_image = tk.PhotoImage(file="View/pictures/bg_map.png")
        
        # Create a canvas and set the background image
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Title
        if site_destination is None:
            title = "Plan a new trip"
        else:
            title = f"Plan a new trip to {site_destination}"
        self.title1 = ctk.CTkLabel(self, text=title, font = ("Impact", 25), text_color='#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 50, window=self.title1)

        # Label entry for the home country
        self.label1 = ctk.CTkLabel(self, text="Choose your departure country", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 80, window=self.label1)

        # Combo box for the departure country
        self.departure_country = ttk.Combobox(self, font=("Arial", 11, 'bold'), values=self.sites_names)
        self.departure_country.configure(state="readonly")
        self.departure_country.set("")
        self.canvas.create_window(250, 110, window=self.departure_country)

        # Label entry for the destination country
        self.label2 = ctk.CTkLabel(self, text="Choose the destination country", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 140, window=self.label2)

        # Combo box for the destination country
        self.destination_country = ttk.Combobox(self, font=("Arial", 11, 'bold'), values=self.sites_names)
        self.destination_country.configure(state="readonly")
        self.destination_country.set("")
        if site_destination is not None:
            self.destination_country.set(site_destination)
            self.destination_country.configure(state="disabled")
        self.canvas.create_window(250, 170, window=self.destination_country)

        # Combo box for the transport
        self.label5 = ctk.CTkLabel(self, text="Choose the transport", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 320, window=self.label5)
        self.transport = ttk.Combobox(self, font=("Arial", 11, 'bold'), values=["Plane", "Train", "Car", "Bus", "Bicycle", "Walking"])
        self.transport.configure(state="readonly")
        self.canvas.create_window(250, 350, window=self.transport)

        # Button to save the trip
        self.button1 = ctk.CTkButton(self, text="Save your trip", font = ("Arial", 11, 'bold'), width = 200, height = 30, fg_color= '#354f52', corner_radius = 10, command=self.save_new_trip)
        self.canvas.create_window(250, 460, window=self.button1)

        self.mainloop()

    def save_new_trip(self):
        """Save the new trip in the database."""
        departure_country = self.departure_country.get()
        destination_country = self.destination_country.get()
        transport = self.transport.get()

        is_valid, message = add_new_trip(self.user.id, departure_country, destination_country, transport, self.sites)

        if not is_valid:
            messagebox.showerror("Error", message)
            self.lift() 
        else:
            self.destroy()
            messagebox.showinfo("Success", message)

            # Refresh the map
            if self.site_destination is None:
                self.master.draw_path()
                self.master.lift()
            else:
                self.master.master.draw_path()
                self.master.master.lift()

    def get_coordinates_by_name(self, name):
        """Get the coordinates of a site by its name."""
        for site in self.sites:
            if site.name == name:
                return site.coordinates
        return None
