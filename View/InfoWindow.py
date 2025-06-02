import tkinter as tk
import customtkinter as ctk

class InfoWindow(tk.Toplevel):
    """
    A window for displaying information about a specific country and planning a new trip.

    Args:
        master: The master widget.
        country_destination: The destination country.

    Attributes:
        country_destination: The destination country.
        user: The current user object.
        title1: Customized label for the title.
        description: Customized label for displaying the country description.
        title_monuments: Customized label for the title of monuments.
        monuments: Customized label for displaying the list of monuments.
        button1: Customized button for planning a new trip.
    """
    def __init__(self, master, name, description):
        super().__init__()
        self.master = master
        self.name = name
        self.description = description
        self.user = master.user
        self.geometry("500x600")
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

        self.mainloop()

    def quit(self):
        """Close the window."""
        self.destroy()