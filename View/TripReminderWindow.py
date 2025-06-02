import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
from tkinter import ttk
from Controller.TripController import get_country_name
from datetime import datetime

class TripReminderWindow(tk.Toplevel):
    """
    A window for displaying reminders of upcoming trips.

    Args:
        master: The master widget.
        reminders: A list of reminders of upcoming trips.

    Attributes:
        master: The master widget.
        reminders: A list of reminders of upcoming trips.
        bg_image: The background image for the window.
        frames: The frames of the animated GIF.
        canvas: Canvas widget for the background image.
        canvas_image: The image object on the canvas.
        current_frame: The current frame of the animated GIF.
        tree: Treeview widget for displaying the reminders.
    """
    def __init__(self, master, reminders):
        super().__init__()
        self.master = master
        self.reminders = reminders
        self.title("Trip Reminder")
        self.resizable(False, False)

        # Load the animated GIF using PIL
        self.bg_image = Image.open("View/pictures/airplane-travel.gif")
        self.frames = [ImageTk.PhotoImage(frame.resize((600, 600), Image.LANCZOS)) for frame in
                   ImageSequence.Iterator(self.bg_image)]

        # Create a canvas to place the background image
        self.canvas = tk.Canvas(self, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw", image=self.frames[0])

        # Start the animation
        self.current_frame = 0
        self.animate()

        # Create and place the table
        self.create_table()

        self.protocol("WM_DELETE_WINDOW", self.on_popup_close) # Handle the window close event, to avoid closing the main window

    def on_popup_close(self):
        """Handle the window close event."""
        self.master.deiconify() # Show the main window
        self.destroy()
        
    def animate(self):
        """Animate the GIF."""
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.canvas.itemconfig(self.canvas_image, image=self.frames[self.current_frame])
        self.after(30, self.animate) # Adjust the delay as needed for the GIF's frame rate

    def create_table(self):
        """Create a table to display the reminders."""
        style = ttk.Style()
        style.configure("mystyle.Treeview",
                        background="#ADD8E6",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#ADD8E6",
                        font=("Arial", 14))
        style.map('mystyle.Treeview', background=[('selected', '#ADD8E6')])

        # Configure the header style
        style.configure("mystyle.Treeview.Heading", 
                        font=("Arial", 14), 
                        background="#ADD8E6", 
                        foreground="black")

        # Create a frame to contain the Treeview
        frame = tk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        # Get the list of trips
        trips = []
        for reminder in self.reminders:
            departure_name = get_country_name(reminder.departure_id)
            destination_name = get_country_name(reminder.destination_id)
            departure_date = datetime.strftime(reminder.departure_date, "%d/%m/%Y")
            return_date = datetime.strftime(reminder.return_date, "%d/%m/%Y")
            trips.append((departure_name, destination_name, departure_date, return_date))

        columns = ('Departure', 'Destination', 'Departure date', 'Return date')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', style="mystyle.Treeview", height=len(trips))
        self.tree.pack(side='top', fill='both', expand=True)

        # Define headings
        self.tree.heading('Departure', text='Departure')
        self.tree.heading('Destination', text='Destination')
        self.tree.heading('Departure date', text='Departure date')
        self.tree.heading('Return date', text='Return date')

        for index, trip in enumerate(trips):
            self.tree.insert('', tk.END, values=trip, tags=('evenrow' if index % 2 == 0 else 'oddrow',))

        # Configure row tags for alternating colors
        self.tree.tag_configure('evenrow', background='#ADD8E6')
        self.tree.tag_configure('oddrow', background='#87CEEB')

        # Adjust column widths
        self.tree.column('Departure', anchor='center', width=150)
        self.tree.column('Destination', anchor='center', width=150)
        self.tree.column('Departure date', anchor='center', width=150)
        self.tree.column('Return date', anchor='center', width=150)
