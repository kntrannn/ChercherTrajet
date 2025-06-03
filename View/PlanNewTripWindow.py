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
        site_destination: The destination site for the trip, if any.
    Attributes:
        master: The master widget.
        user: The current user object.
        sites: A list of available sites.
        sites_names: A list of names of the available sites.
        site_destination: The destination site for the trip, if any.
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
        self.canvas = tk.Canvas(self, width=500, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Title
        self.title1 = ctk.CTkLabel(self, text="Plan a new trip", font = ("Impact", 25), text_color='#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 50, window=self.title1)

        # Label entry for the home country
        self.label1 = ctk.CTkLabel(self, text="Choose your departure site", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 80, window=self.label1)

        # Combo box for the departure country
        self.departure_country = ttk.Combobox(self, font=("Arial", 11, 'bold'), values=self.sites_names)
        self.departure_country.configure(state="readonly")
        self.departure_country.set("")
        self.canvas.create_window(250, 110, window=self.departure_country)

        # Label entry for the destination country
        self.label2 = ctk.CTkLabel(self, text="Choose the destination site", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 140, window=self.label2)

        # Combo box for the destination country
        self.destination_country = ttk.Combobox(self, font=("Arial", 11, 'bold'), values=self.sites_names)
        self.destination_country.configure(state="readonly")
        self.destination_country.set("")
        if site_destination is not None:
            self.destination_country.set(site_destination)
            self.destination_country.configure(state="disabled")
        self.canvas.create_window(250, 170, window=self.destination_country)

        # Combo box for the vehicle
        self.label5 = ctk.CTkLabel(self, text="Choose the vehicle", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.canvas.create_window(250, 200, window=self.label5)
        self.transport = ttk.Combobox(self, font=("Arial", 11, 'bold'), values=["Plane", "Train", "Car", "Bus", "Bicycle", "Walking"])
        self.transport.configure(state="readonly")
        self.canvas.create_window(250, 230, window=self.transport)

        # Button to save the trip
        self.button1 = ctk.CTkButton(self, text="Save your trip", font = ("Arial", 11, 'bold'), width = 200, height = 30, fg_color= '#354f52', corner_radius = 10, command=self.save_new_trip)
        self.canvas.create_window(250, 340, window=self.button1)

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
            self.master.draw_path()
            self.master.lift()