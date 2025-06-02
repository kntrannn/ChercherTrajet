import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from tkinter import messagebox
from Model.Map import Map
from View.InfoWindow import InfoWindow
from Controller.MapController import get_all_communes_with_x_y, get_all_filtered_sites_with_x_y, get_centroid, list_depth, get_all_trips
class MapWindow(tk.Tk):
    """
    A window for displaying the personal world map and providing options for trip planning and management.

    Attributes:
        user: The current user object.
        canevas: The zoomable canvas for displaying the map.
        map: The map object containing country coordinates.
        bg_image: The background image for the animated map.
        frames: The frames of the animated map.
        quit_button: Button to quit the application.
        side_bar: Frame for displaying side bar buttons.
        top_spacer: Spacer frame to position side bar buttons.
        canva: Canvas for displaying icons on the top.
        button1: Button to show all trips.
        button2: Button to plan a new trip.
        button3: Button to change password.
        button4: Button to sign out.
        bottom_spacer: Spacer frame to position side bar buttons.
        current_frame: The current frame of the animated map.
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

        # Load the animated GIF using PIL
        self.bg_image = Image.open("View/pictures/waves_map.gif")
        self.frames = [ImageTk.PhotoImage(frame.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.LANCZOS)) for frame in
                   ImageSequence.Iterator(self.bg_image)]

        # Quit button
        self.quit_button = ctk.CTkButton(self, text="Quit", text_color= "#f5f6f9", fg_color= '#354f52', font=("Arial", 28, "bold"), hover_color = "#e2eafc", border_color = '#354f52')
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
        self.button2 = ctk.CTkButton(self.side_bar, text="cc j do", text_color="#f5f6f9", fg_color= "transparent", font=("Arial", 15, "bold"), hover_color = "#e2eafc",border_color = "#f5f6f9", corner_radius= 32, height=2, image = ctk.CTkImage(dark_image=icon3, light_image=icon3))
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

    def quit(self, event):
        """Close the window."""
        self.destroy()

    def sign_out(self):
        """Sign out the user and open the login window."""
        from View.SignInWindow import LoginWindow
        self.destroy()
        LoginWindow()

    def draw_communes(self):
        """Draw the map with visited and to-visit countries highlighted, centered at the canvas center."""
        self.canevas.delete("all")
        self.canevas.update_idletasks() # Update the canvas before drawing
        canvas_width = self.winfo_screenwidth()
        canvas_height = self.winfo_screenheight()
        cx, cy = self.centroid
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        scale = 52 # Adjust the scale factor as needed

        for commune in self.communes:
            v = commune.coordinates
            name = commune.name
            description = commune.description
            depth = list_depth(v)

            if depth == 4:  # Country of multiple polygons
                for ele in v:
                    for ele2 in ele:
                        shifted = [((x - cx) * scale + canvas_center_x, (y - cy) * scale + canvas_center_y) for x, y in ele2]
                        polygon = self.canevas.create_polygon(shifted, fill="#354f52", outline="white")
                        self.canevas.tag_bind(polygon, "<Double-Button-1>", lambda e, n=name, d=description: self.show_info(n, d))
            elif depth == 3:  # Country of one polygon
                for ele in v:
                    shifted = [((x - cx) * scale + canvas_center_x, (y - cy) * scale + canvas_center_y) for x, y in ele]
                    polygon = self.canevas.create_polygon(shifted, fill="#354f52", outline="white")
                    self.canevas.tag_bind(polygon, "<Double-Button-1>", lambda e, n=name, d=description: self.show_info(n, d))

    def show_info(self, name, description):
        if description == "":
            description = "No description available."
        InfoWindow(self, name, description)

    def draw_sites(self):
        """Draw the sites on the map, centered and scaled like the draw_communes method."""
        self.canevas.update_idletasks()
        canvas_width = self.winfo_screenwidth()
        canvas_height = self.winfo_screenheight()
        cx, cy = self.centroid
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        scale = 52

        for site in self.sites:
            # The coordinates of the site are in the form (x, y)
            x, y = site.coordinates
            name = site.name
            description = site.description
            shifted = ((x - cx) * scale + canvas_center_x, (y - cy) * scale + canvas_center_y)
            point = self.canevas.create_oval(shifted[0] - 5, shifted[1] - 5, shifted[0] + 5, shifted[1] + 5, fill="red")
            self.canevas.tag_bind(point, "<Double-Button-1>", lambda e, n=name, d=description: self.show_info(n, d))

    def draw_path(self):
        """Draw a path on the map, centered and scaled like the draw_communes method."""
        self.canevas.update_idletasks()
        canvas_width = self.winfo_screenwidth()
        canvas_height = self.winfo_screenheight()
        cx, cy = self.centroid
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        scale = 52

        trips = get_all_trips(self.user.id, canvas_width, canvas_height)
        for trip in trips:
            path = trip.sites_visited
            for i in range(len(path) - 1):
                x1, y1 = path[i].coordinates
                x2, y2 = path[i + 1].coordinates
                shifted1 = ((x1 - cx) * scale + canvas_center_x, (y1 - cy) * scale + canvas_center_y)
                shifted2 = ((x2 - cx) * scale + canvas_center_x, (y2 - cy) * scale + canvas_center_y)
                self.canevas.create_line(shifted1[0], shifted1[1], shifted2[0], shifted2[1], fill="yellow", width=2)

                # Draw circle at every point in the path
                if i == 0:
                    self.canevas.create_oval(shifted1[0] - 5, shifted1[1] - 5, shifted1[0] + 5, shifted1[1] + 5, fill="blue")
                elif i == len(path) - 2:
                    self.canevas.create_oval(shifted1[0] - 5, shifted1[1] - 5, shifted1[0] + 5, shifted1[1] + 5, fill="green")
                    self.canevas.create_oval(shifted2[0] - 5, shifted2[1] - 5, shifted2[0] + 5, shifted2[1] + 5, fill="blue")
                else:
                    self.canevas.create_oval(shifted1[0] - 5, shifted1[1] - 5, shifted1[0] + 5, shifted1[1] + 5, fill="green")

    def change_password(self, event):
        """Open the window for changing the password."""
        from View.ChangePasswordWindow import ChangePasswordWindow
        ChangePasswordWindow(self)