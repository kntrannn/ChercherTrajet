import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from tkinter import messagebox
from Map import Map

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

        # Quit button
        self.quit_button = ctk.CTkButton(self, text="Quit", text_color= "#f5f6f9", fg_color= '#354f52', font=("Arial", 28, "bold"), hover_color = "#e2eafc", border_color = '#354f52')
        self.quit_button.bind("<Button-1>", self.quit)
        self.quit_button.pack(side="top", fill="x")

        # Map
        self.canevas = tk.Canvas(self, bg="#e2eafc", width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.canevas.pack(side="top", fill="both", expand=True)
        self.map = Map(self.winfo_screenwidth(), self.winfo_screenheight())
        self.draw()
        # self.draw_sites()

        self.mainloop()

    def quit(self, event):
        """Close the window."""
        self.destroy()

    def draw(self):
        """Draw the map with visited and to-visit countries highlighted, centered at the canvas center."""
        # self.canevas.delete("all")
        # self.canevas.update_idletasks() # Update the canvas before drawing
        canvas_width = self.winfo_screenwidth()
        canvas_height = self.winfo_screenheight()
        cx, cy = self.compute_centroid(self.map.coordinates_dict)
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        scale = 55 # Adjust the scale factor as needed

        for (k, v) in self.map.coordinates_dict.items():
            depth = self.map.list_depth(v)

            if depth == 4:  # Country of multiple polygons
                for ele in v:
                    for ele2 in ele:
                        shifted = [((x - cx) * scale + canvas_center_x, (y - cy) * scale + canvas_center_y) for x, y in ele2]
                        self.canevas.create_polygon(shifted, fill="#354f52", outline="white")
            elif depth == 3:  # Country of one polygon
                for ele in v:
                    shifted = [((x - cx) * scale + canvas_center_x, (y - cy) * scale + canvas_center_y) for x, y in ele]
                    self.canevas.create_polygon(shifted, fill="#354f52", outline="white")

    def compute_centroid(self, coords_dict):
        all_points = []
        for v in coords_dict.values():
            depth = self.map.list_depth(v)
            if depth == 4:
                for ele in v:
                    for ele2 in ele:
                        all_points.extend(ele2)
            elif depth == 3:
                for ele in v:
                    all_points.extend(ele)
        
        if not all_points:
            return 0, 0
        xs = [x for x, y in all_points]
        ys = [y for x, y in all_points]
        return sum(xs)/len(xs), sum(ys)/len(ys)
    
    def compute_centroid_sites(self, sites):
        all_points = list(sites.values())
        xs = [x for x, y in all_points]
        ys = [y for x, y in all_points]
        return sum(xs)/len(xs), sum(ys)/len(ys)

    def draw_sites(self):
        """Draw the sites on the map, centered and scaled like the draw() function."""
        self.canevas.update_idletasks()
        canvas_width = self.winfo_screenwidth()
        canvas_height = self.winfo_screenheight()
        cx, cy = self.compute_centroid_sites(self.map.sites)
        print(cx, cy)
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        scale = 55

        for (k, v) in self.map.sites.items():
            # The coordinates of the site are in the form (x, y)
            x, y = v
            shifted = ((x - cx) * scale + canvas_center_x, (y - cy) * scale + canvas_center_y)
            self.canevas.create_oval(shifted[0] - 3, shifted[1] - 3, shifted[0] + 3, shifted[1] + 3, fill="red")

if __name__ == "__main__":
    # Example usage
    class User:
        def __init__(self, id):
            self.id = id

    user = User(id=1)
    app = MapWindow(user)