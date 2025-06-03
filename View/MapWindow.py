import tkinter as tk
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from Model.Map import Map
from View.InfoWindow import InfoWindow
from View.TripDetailsWindow import TripDetailsWindow
from View.ShowAllTripsWindow import ShowAllTripsWindow
from Controller.MapController import get_all_communes_with_x_y, get_all_filtered_sites_with_x_y, get_centroid, list_depth, get_all_trips

class MapWindow(tk.Tk):
    """
    A window that displays a personal world map with the user's visited and to-visit countries, sites, and trips.
    Args:
        user: The current user object.
    Attributes:
        user: The current user object.
        sites: A list of all filtered sites with coordinates.
        bg_image: The background image for the map.
        frames: A list of frames for the animated background.
        canva: A canvas for displaying the map and sites.
        communes: A list of all communes with coordinates.
        centroid: The centroid of all communes and sites.
    """
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.attributes("-fullscreen", True)
        self.title("Personal World Map")

        self.sites = get_all_filtered_sites_with_x_y(self.winfo_screenwidth(), self.winfo_screenheight(), min_distance=0.5)

        # ICONS
        icon1 = tk.PhotoImage(file="View/pictures/map_icon.png")
        icon2 = Image.open("View/pictures/icon_suitcase.png")
        icon3 = Image.open("View/pictures/plan_icon.png")
        icon4 = Image.open("View/pictures/pw_icon.png")
        icon5 = Image.open("View/pictures/log_out_icon.png")
        icon6 = Image.open("View/pictures/quit_icon.png")

        # Quit button
        self.quit_button = ctk.CTkButton(self, text="Quit", text_color= "#f5f6f9", fg_color= '#354f52', font=("Arial", 28, "bold"), hover_color = "#e2eafc", border_color = '#354f52', image=ctk.CTkImage(dark_image=icon6, light_image=icon6))
        self.quit_button.bind("<Button-1>", self.quit)
        self.quit_button.pack(side="top", fill="x")

        # Side bar containing 3 buttons
        self.side_bar = ctk.CTkFrame(self, fg_color='#354f52', border_color = '#354f52')
        self.side_bar.pack(side="right", fill="y")

        # Spacer frame to push buttons to the center
        self.top_spacer = ctk.CTkFrame(self.side_bar, fg_color='#354f52', border_color = '#354f52')
        self.top_spacer.pack(side="top", expand=True)

        # Icon on top
        self.canva = ctk.CTkCanvas(self.top_spacer, bg='#354f52', highlightthickness = 0)
        self.canva.pack(expand="YES")
        self.canva.create_image(self.canva.winfo_reqwidth()/2, self.canva.winfo_reqheight()/2, image=icon1, anchor = "center")

        # Button to show all trips
        self.button1 = ctk.CTkButton(self.side_bar, text="Plan a new trip", text_color="#f5f6f9", fg_color= "transparent", border_color = "#f5f6f9", hover_color = "#e2eafc", corner_radius= 32,   font=("Arial", 15, "bold") ,height=2, image = ctk.CTkImage(dark_image=icon2, light_image=icon2))
        self.button1.bind("<Button-1>", self.open_plan_new_trip_window)
        self.button1.pack(side="top", pady=10, padx=10)

        # Button to plan a new trip
        self.button2 = ctk.CTkButton(self.side_bar, text="Show all trips", text_color="#f5f6f9", fg_color= "transparent", font=("Arial", 15, "bold"), hover_color = "#e2eafc",border_color = "#f5f6f9", corner_radius= 32, height=2, image = ctk.CTkImage(dark_image=icon3, light_image=icon3))
        self.button2.bind("<Button-1>", self.open_show_all_trips_window)
        self.button2.pack(side="top", pady=10, padx=10)

        # Button to change password
        self.button3 = ctk.CTkButton(self.side_bar, text="Change password", text_color="#f5f6f9", fg_color= "transparent", font=("Arial", 15, "bold"), hover_color = "#e2eafc",border_color = "#f5f6f9", corner_radius= 32, height=2, image = ctk.CTkImage(dark_image=icon4, light_image=icon4))
        self.button3.bind("<Button-1>", lambda event: self.change_password(event))
        self.button3.pack(side="top", pady=10, padx=10)

        # Button to sign out
        self.button4 = ctk.CTkButton(self.side_bar, text="Sign out", text_color="#f5f6f9", fg_color= "transparent", font=("Arial", 15, "bold"), hover_color = "#e2eafc",border_color = "#f5f6f9", corner_radius= 32,  height=2, image = ctk.CTkImage(dark_image=icon5, light_image=icon5))
        self.button4.bind("<Button-1>", lambda event: self.sign_out())
        self.button4.pack(side="bottom", pady=10, padx=10)

        # Spacer frame to keep buttons in the center
        self.bottom_spacer = ctk.CTkFrame(self.side_bar, fg_color='#354f52')
        self.bottom_spacer.pack(side="top", expand=True)

        # Map
        self.canevas = tk.Canvas(self, bg="#e2eafc", width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.map = Map(self.winfo_screenwidth(), self.winfo_screenheight())
        self.communes = get_all_communes_with_x_y(self.winfo_screenwidth(), self.winfo_screenheight())
        self.centroid = get_centroid(self.communes, self.sites)
        self.draw_communes()
        self.draw_sites()
        self.draw_path()
        self.canevas.pack(side="left")

        self.mainloop()

    def open_plan_new_trip_window(self, event):
        """Open the window for planning a new trip."""
        from View.PlanNewTripWindow import PlanNewTripWindow
        PlanNewTripWindow(self, None)

    def open_show_all_trips_window(self, event):
        """Open the window for showing all trips."""
        ShowAllTripsWindow(self, self.sites)

    def quit(self, event):
        """Close the window."""
        self.destroy()

    def sign_out(self):
        """Sign out the user and open the login window after confirmation."""
        if messagebox.askyesno("Confirm Sign Out", "Are you sure you want to sign out?"):
            from View.SignInWindow import LoginWindow
            self.destroy()
            LoginWindow()

    def draw_communes(self):
        """Draw the communes on the map, centered and scaled to fit the canvas."""
        self.canevas.delete("all")
        canvas_width = self.winfo_screenwidth()
        canvas_height = self.winfo_screenheight()
        cx, cy = self.centroid
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        scale = 52 # Adjust the scale factor as needed

        for commune in self.communes:
            v = commune.coordinates_canvas
            name = commune.name
            description = commune.description
            depth = list_depth(v)

            if depth == 4:  # Country of multiple polygons
                for ele in v:
                    for ele2 in ele:
                        shifted = [((x - cx) * scale + canvas_center_x, (y - cy) * scale + canvas_center_y) for x, y in ele2]
                        polygon = self.canevas.create_polygon(shifted, fill="#354f52", outline="white")
                        self.canevas.tag_bind(polygon, "<Double-Button-1>", lambda e, n=name, d=description: self.show_info(n, d, False))
            elif depth == 3:  # Country of one polygon
                for ele in v:
                    shifted = [((x - cx) * scale + canvas_center_x, (y - cy) * scale + canvas_center_y) for x, y in ele]
                    polygon = self.canevas.create_polygon(shifted, fill="#354f52", outline="white")
                    self.canevas.tag_bind(polygon, "<Double-Button-1>", lambda e, n=name, d=description: self.show_info(n, d, False))

    def show_info(self, name, description, is_site):
        """Open an information window for a specific commune or site."""
        if description == "":
            description = "No description available."
        InfoWindow(self, name, description, is_site)

    def draw_sites(self):
        """Draw the sites on the map, centered and scaled like the draw_communes method."""
        canvas_width = self.winfo_screenwidth()
        canvas_height = self.winfo_screenheight()
        cx, cy = self.centroid
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        scale = 52

        for site in self.sites:
            x, y = site.coordinates_canvas
            name = site.name
            description = site.description
            shifted = ((x - cx) * scale + canvas_center_x, (y - cy) * scale + canvas_center_y)
            if name == "Ludivisites Lyon":
                point = self.canevas.create_oval(shifted[0] - 5, shifted[1] - 5, shifted[0] + 5, shifted[1] + 5, fill="purple")
            else:
                point = self.canevas.create_oval(shifted[0] - 5, shifted[1] - 5, shifted[0] + 5, shifted[1] + 5, fill="red")
            self.canevas.tag_bind(point, "<Double-Button-1>", lambda e, n=name, d=description: self.show_info(n, d, True))

    def draw_path(self):
        """Draw the paths of all trips on the map, connecting sites with lines and marking start and end points."""
        canvas_width = self.winfo_screenwidth()
        canvas_height = self.winfo_screenheight()
        cx, cy = self.centroid
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        scale = 52

        trips = get_all_trips(self.user.id, self.sites)
        for trip in trips:
            path = trip.sites_visited
            name_start = trip.start_site.name
            name_end = trip.end_site.name
            description_start = trip.start_site.description
            description_end = trip.end_site.description
            for i in range(len(path) - 1):
                x1, y1 = path[i].coordinates_canvas
                x2, y2 = path[i + 1].coordinates_canvas
                shifted1 = ((x1 - cx) * scale + canvas_center_x, (y1 - cy) * scale + canvas_center_y)
                shifted2 = ((x2 - cx) * scale + canvas_center_x, (y2 - cy) * scale + canvas_center_y)

                if i == 0:
                    site = self.canevas.create_oval(shifted1[0] - 5, shifted1[1] - 5, shifted1[0] + 5, shifted1[1] + 5, fill="cyan")
                    self.canevas.tag_bind(site, "<Double-Button-1>", lambda e, n=name_start, d=description_start: self.show_info(n, d, True))
                elif i == len(path) - 2:
                    site = self.canevas.create_oval(shifted2[0] - 5, shifted2[1] - 5, shifted2[0] + 5, shifted2[1] + 5, fill="blue")
                    self.canevas.tag_bind(site, "<Double-Button-1>", lambda e, n=name_end, d=description_end: self.show_info(n, d, True))

                line = self.canevas.create_line(shifted1[0], shifted1[1], shifted2[0], shifted2[1], fill="yellow", width=4)
                self.canevas.tag_bind(line, "<Double-Button-1>", lambda e, t=trip: self.show_trip_details(t))

    def show_trip_details(self, trip):
        """Open the trip details window for a specific trip."""
        TripDetailsWindow(self, trip)

    def change_password(self, event):
        """Open the window for changing the password."""
        from View.ChangePasswordWindow import ChangePasswordWindow
        ChangePasswordWindow(self)