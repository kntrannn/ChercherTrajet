import tkinter as tk
import customtkinter as ctk

class TripDetailsWindow(tk.Toplevel):
    """
    A window that displays detailed information about a specific trip.
    Args:
        master: The master widget.
        trip: The trip object containing details about the trip.
    Attributes:
        master: The master widget.
        trip: The trip object containing details about the trip.
        user: The current user object.
        start_name: The name of the starting site of the trip.
        end_name: The name of the ending site of the trip.
        vehicle: The vehicle used for the trip.
        distance: The distance of the trip in kilometers.
        carbon_footprint: The carbon footprint of the trip in kilograms of CO2.
        sites_visited: A list of names of sites visited during the trip.
    """
    def __init__(self, master, trip):
        super().__init__()
        self.master = master
        self.trip = trip
        self.user = master.user
        self.geometry("600x450")
        self.resizable(False, False)
        self.title("Trip from " + self.trip.start_site.name + " to " + self.trip.end_site.name)
        self.config(bg="#f5f6f9")
        self.start_name = self.trip.start_site.name
        self.end_name = self.trip.end_site.name
        self.vehicle = self.trip.vehicle
        self.distance = round(self.trip.distance, 2)
        self.carbon_footprint = round(self.trip.carbon_footprint, 2)
        self.sites_visited = [site.name for site in self.trip.sites_visited]
        self.create_widgets()

        self.mainloop()

    def create_widgets(self):
        """Create the widgets for the trip details window."""
        # Title
        title = f'{self.start_name} to {self.end_name}'
        self.title1 = ctk.CTkLabel(self, text=f'{title}', text_color='#354f52', fg_color="#f5f6f9",
                                    corner_radius=32, font=("Impact", 22), height=2)
        self.title1.pack(side="top", padx=20, pady=20)

        self.vehicle_label = ctk.CTkLabel(self, text=f'Vehicle: {self.vehicle}', text_color="#354f52",
                                          fg_color='#f5f6f9', corner_radius=32, font=("Arial", 16, "bold"),
                                          height=30, width=450)
        self.vehicle_label.pack(side="top", padx=20, pady=5)
        self.distance_label = ctk.CTkLabel(self, text=f'Distance: {self.distance} km', text_color="#354f52",
                                           fg_color='#f5f6f9', corner_radius=32, font=("Arial", 16, "bold"),
                                           height=30, width=450)
        self.distance_label.pack(side="top", padx=20, pady=5)
        self.carbon_label = ctk.CTkLabel(self, text=f'Carbon Footprint: {self.carbon_footprint} kg CO2',
                                         text_color="#354f52", fg_color='#f5f6f9', corner_radius=32,
                                         font=("Arial", 16, "bold"), height=30, width=450)
        self.carbon_label.pack(side="top", padx=20, pady=5)
        self.sites_label = ctk.CTkLabel(self, text='Sites Visited:', text_color="#354f52",
                                        fg_color='#f5f6f9', corner_radius=32, font=("Arial", 16, "bold"),
                                        height=30, width=450)
        self.sites_label.pack(side="top", padx=20, pady=5)
        self.sites_visited_label = ctk.CTkLabel(self, text=', '.join(self.sites_visited), text_color="#354f52",
                                                 fg_color='#f5f6f9', corner_radius=32, font=("Arial", 16),
                                                 height=30, width=600, wraplength=500)
        self.sites_visited_label.pack(side="top", padx=20, pady=5)