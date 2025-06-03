import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from Controller.MapController import get_all_trips
from View.TripDetailsWindow import TripDetailsWindow

class ShowAllTripsWindow(tk.Toplevel):
    """
    A window that displays all trips of the user in a treeview format.
    Args:
        master: The master widget.
        sites: A list of available sites.
    Attributes:
        master: The master widget.
        user: The current user object.
        trips: A list of all trips associated with the user.
    """
    def __init__(self, master, sites):
        ctk.set_appearance_mode("light")

        super().__init__()
        self.master = master
        self.user = master.user
        self.title("All my trips")
        self.resizable(False, False)
        self.geometry("1000x450")

        self.trips = get_all_trips(self.user.id, sites)

        # Title label
        title = ctk.CTkLabel(self, text="All my trips", font=("Arial", 30, "bold"), text_color="#f5f6f9", bg_color="#f5f6f9", fg_color="#354f52")
        title.pack(side="top", fill="x")

        self.show_trips()

        self.mainloop()

    def show_trips(self):
        """Display all trips in a treeview format."""
        # Display upcoming trips in form of treeview
        self.trip_tree = ttk.Treeview(self)
        # Single choice
        self.trip_tree["selectmode"] = "browse"
        self.trip_tree["columns"] = ("departure", "destination", "vehicle", "distance", "carbon_footprint", "visited_sites")
        self.trip_tree.column("#0", width=0, stretch=tk.NO)
        self.trip_tree.column("departure", anchor=tk.W, width=300, stretch=tk.NO)
        self.trip_tree.column("destination", anchor=tk.W, width=300, stretch=tk.NO)
        self.trip_tree.column("vehicle", anchor=tk.W, width=100, stretch=tk.NO)
        self.trip_tree.column("distance", anchor=tk.W, width=100, stretch=tk.NO)
        self.trip_tree.column("carbon_footprint", anchor=tk.W, width=200, stretch=tk.NO)
        self.trip_tree.heading("#0", text="", anchor=tk.W)
        self.trip_tree.heading("departure", text="Departure", anchor=tk.W)
        self.trip_tree.heading("destination", text="Destination", anchor=tk.W)
        self.trip_tree.heading("vehicle", text="Vehicle", anchor=tk.W)
        self.trip_tree.heading("distance", text="Distance (in km)", anchor=tk.W)
        self.trip_tree.heading("carbon_footprint", text="Carbon footprint (in kg)", anchor=tk.W)

        for trip in self.trips:
            start_site = trip.start_site.name
            end_site = trip.end_site.name
            vehicle = trip.vehicle
            distance = round(trip.distance, 2)
            carbon_footprint = round(trip.carbon_footprint, 2)

            # Building the treeview
            self.trip_tree.insert("", "end", values=(start_site, end_site, vehicle, distance, carbon_footprint))

        # Add a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.trip_tree.yview)
        self.trip_tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        # Bind double-click event to show trip details
        self.trip_tree.bind("<Double-1>", lambda event: TripDetailsWindow(self.master, self.trips[self.trip_tree.index(self.trip_tree.selection())]))

        # Pack the treeview
        self.trip_tree.pack(side="top", fill="both", expand=True)