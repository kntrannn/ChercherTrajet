import tkinter as tk
import customtkinter as ctk

class InfoWindow(tk.Toplevel):
    """
    A window that displays information about a specific site or trip.
    Args:
        master: The master widget.
        name: The name of the site or trip.
        description: A description of the site or trip.
    Attributes:
        master: The master widget.
        name: The name of the site or trip.
        description: A description of the site or trip.
        user: The current user object.
    """
    def __init__(self, master, name, description, is_site):
        super().__init__()
        self.master = master
        self.name = name
        self.description = description
        self.user = master.user
        self.geometry("500x360")
        self.resizable(False, False)
        self.title("Information about " + self.name)
        self.config(bg="#f5f6f9")

        # Title
        self.title1 = ctk.CTkLabel(self, text=f'{self.name}', text_color='#354f52', fg_color="#f5f6f9",
                                    corner_radius=32, font=("Impact", 22), height=2)
        self.title1.pack(side="top", padx=20, pady=20)

        # Description
        self.description = ctk.CTkLabel(self, text=description, text_color="#f5f6f9",
                                         fg_color='#354f52', corner_radius=32, font=("Arial", 12, "bold"),
                                         height=200, width=450, wraplength=400)
        self.description.pack(side="top")

        if is_site:
            # Button to plan a trip
            self.button1 = ctk.CTkButton(self, text=f"Plan a trip to {self.name}",
                                        font=("Arial", 14, 'bold'), width=200, height=30, fg_color='#c06848',
                                        corner_radius=10)
            self.button1.pack(side="top", padx=20, pady=20)
            self.button1.bind("<Button-1>", self.plan_trip)

        self.mainloop()

    def plan_trip(self, event):
        """
        Callback function for the button to plan a trip.
        It unbinds the button to prevent multiple clicks and opens the PlanNewTripWindow.
        """
        self.button1.unbind("<Button-1>")
        self.after(100, self.open_plan_new_trip)

    def open_plan_new_trip(self):
        """
        Opens the PlanNewTripWindow with the current user's name as the destination site.
        """
        self.destroy()
        from View.PlanNewTripWindow import PlanNewTripWindow
        PlanNewTripWindow(self.master, self.name)